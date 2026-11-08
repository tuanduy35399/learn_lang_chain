import base64
import mimetypes
from tkinter import TclError, Tk, filedialog
from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()


def choose_image_file() -> Path:
    """Open a local file picker when no image path is passed on the command line."""
    root = None
    try:
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        filename = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.webp"),
                ("All files", "*.*"),
            ],
        )
    except TclError:
        filename = input("Image path: ").strip().strip('"').strip("'")
    finally:
        if root is not None:
            root.destroy()

    if not filename:
        raise SystemExit("No image selected.")

    return Path(filename).expanduser()

def image_to_data_url(image_path: Path) -> str:
    image_path = image_path.expanduser().resolve()

    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    mime_type, _ = mimetypes.guess_type(str(image_path))
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError(f"Not an image file: {image_path}")

    image_b64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{image_b64}"

def build_image_message(image_path: Path, prompt) -> HumanMessage:
    return HumanMessage(
        content=[
            {"type": "text", "text": "prompt"},
            {"type": "image_url", "image_url": {"url": image_to_data_url(image_path)}},
        ]
    )

model= ChatOpenAI(model="my_models", base_url="http://localhost:20128/v1", temperature=1.0)
agent = create_agent(model=model)

img_path = choose_image_file()
message= build_image_message(image_path=img_path, prompt="Tam hinh nay dang co gi, noi ve cai gi, dung tieng Viet di ban")

respone= agent.invoke(
    {
        "messages": message,
    }
)
print(respone["messages"][-1].content)

