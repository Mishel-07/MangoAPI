# MangoAPI
A simple Python client for Mango 🥭. Mango is a simple API that you can use for AI, text generation (LLM), image generation, and more. If you have any queries or need support, reach out at https://t.me/XBOTSUPPORTS.

## Installation

Install MangoAPI using pip:
```bash
pip install mangoapi
```

## Usage

Here is a basic example of how to use MangoAPI:

```python
from mango import Mango

client = Mango()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

print(response.choices[0].message.content)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact
For support or inquiries, please reach out to us at [Telegram Support](https://t.me/XBOTSUPPORTS).

