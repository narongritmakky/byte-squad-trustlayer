import argparse
from .db.database import SessionLocal
from .services import inventory_service
from .utils.logger import get_logger

logger = get_logger("inventrack.cli")

def cmd_restock(args):
    db = SessionLocal()
    if args.quantity <= 0:
        # BUG #8: return ตรงนี้โดยไม่ db.close() — connection รั่วออกจาก pool
        # ทุกครั้งที่ผู้ใช้ป้อน quantity ที่ไม่เป็นบวกผ่าน CLI
        logger.error("Quantity must be positive")
        return
    try:
        inventory_service.restock(db, args.product_id, args.quantity)
        logger.info(f"Restocked product {args.product_id} by {args.quantity}")
    finally:
        db.close()

def build_parser():
    parser = argparse.ArgumentParser(prog="inventrack")
    subparsers = parser.add_subparsers(dest="command", required=True)

    restock_parser = subparsers.add_parser("restock", help="Add stock to a product")
    restock_parser.add_argument("product_id", type=int)
    restock_parser.add_argument("quantity", type=int)
    restock_parser.set_defaults(func=cmd_restock)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
