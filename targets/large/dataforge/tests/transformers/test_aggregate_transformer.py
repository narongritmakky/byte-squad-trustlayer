import pytest
from dataforge.transformers.aggregate_transformer import AggregateTransformer

def test_avg_with_none_values_raises_or_skews(sample_records):
    # ทดสอบ BUG #5: ค่า None ใน amount ทำให้ sum()/avg() พัง หรือให้ผลผิด
    transformer = AggregateTransformer(group_by="region", agg_field="amount", agg_func="avg")
    with pytest.raises(TypeError):
        transformer.transform(sample_records)  # US group มี [100.0, None] -> TypeError
