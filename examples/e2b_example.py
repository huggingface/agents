from smolagents import Tool, CodeAgent, HfApiEngine
from smolagents.default_tools import VisitWebpageTool
from dotenv import load_dotenv

load_dotenv()

class GetCatImageTool(Tool):
    name="get_cat_image"
    description = "Get a cat image"
    inputs = {}
    output_type = "image"

    def __init__(self):
        super().__init__()
        self.url = "https://em-content.zobj.net/source/twitter/53/robot-face_1f916.png"

    def forward(self):
        from PIL import Image
        import requests
        from io import BytesIO

        response = requests.get(self.url)

        return Image.open(BytesIO(response.content))

LAUNCH_GRADIO = False

get_cat_image = GetCatImageTool()


agent = CodeAgent(
    tools = [get_cat_image, VisitWebpageTool()],
    llm_engine=HfApiEngine(),
    additional_authorized_imports=["Pillow", "requests", "markdownify"], # "duckduckgo-search", 
    use_e2b_executor=False
)

if LAUNCH_GRADIO:
    from smolagents import GradioUI

    GradioUI(agent).launch()
else:
    agent.run(
        "Return me an image of Lincoln's preferred pet",
        additional_context="Here is a webpage about US presidents and pets: https://www.9lives.com/blog/a-history-of-cats-in-the-white-house/"
    )
