import pandas as pd

from modules.report_generator import ReportGenerator


def test_report_generator_accepts_output_path_argument(tmp_path):
    df = pd.DataFrame({"numeric": [1, 2, 3], "category": ["a", "b", "c"]})
    output_path = tmp_path / "report.html"

    generated_path = ReportGenerator(df).generate(
        output_path=str(output_path),
        statistics=df.describe(),
        insights=["Dataset looks reasonably clean."],
    )

    assert generated_path == str(output_path)
    assert output_path.exists()
    assert "Autonomous Data Analyst Report" in output_path.read_text(encoding="utf-8")
