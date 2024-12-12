import pytest
from readii.io.utils import PatternResolver, PatternResolverError # type: ignore

@pytest.mark.parametrize("pattern, context, expected", [
  ("{subject_id}_{date}/{disease}.txt", {"subject_id": "JohnDoe", "date": "2025-01-01", "disease": "cancer"}, "JohnDoe_2025-01-01/cancer.txt"),
  ("{subject_id}_{date}/{disease}.txt", {"subject_id": "JohnDoe", "date": "2025-01-01"}, PatternResolverError),
  ("{subject_id}_{date}/{disease.txt", {}, PatternResolverError),
  # New complex test cases
  ("{subject_id}_{date}/{disease}/{sample_id}.txt", {"subject_id": "JaneDoe", "date": "2025-01-01", "disease": "flu", "sample_id": "S123"}, "JaneDoe_2025-01-01/flu/S123.txt"),
  ("{subject_id}_{date}/{disease}/{sample_id}.txt", {"subject_id": "JaneDoe", "date": "2025-01-01", "disease": "flu"}, PatternResolverError),
  ("{subject_id}_{date}/{disease}/{sample_id}.txt", {"subject_id": "JaneDoe", "date": "2025-01-01", "disease": "flu", "sample_id": ""}, "JaneDoe_2025-01-01/flu/.txt"),
  ("{subject_id}_{date}/{disease}/{sample_id}.txt", {"subject_id": "JaneDoe", "date": "2025-01-01", "disease": "flu", "sample_id": None}, PatternResolverError),
  ("{subject_id}_{date}/{disease}/{sample_id}.txt", {"subject_id": "JaneDoe", "date": "2025-01-01", "disease": "flu", "sample_id": "S123", "extra_key": "extra_value"}, "JaneDoe_2025-01-01/flu/S123.txt"),
])
def test_resolve(pattern, context, expected):
  if isinstance(expected, type) and issubclass(expected, Exception):
    with pytest.raises(expected):
      resolver = PatternResolver(pattern)
      resolver.resolve(context)
  else:
    resolver = PatternResolver(pattern)
    result = resolver.resolve(context)
    assert result == expected
