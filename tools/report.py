from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel

def write_report(filename, html):
    with open(filename, 'w') as f:
        f.write(html)

class WriteReportArgsSchema(BaseModel):
    filename: str
    html: str

#using structuredTool so that the tool can receive multiple arguments
write_report_tool = StructuredTool.from_function(
    name="Write report",
    description="Write an HTML file to disk. Use this tool whenever whenever user asks for a report",
    func=write_report,
    args_schema=WriteReportArgsSchema
)