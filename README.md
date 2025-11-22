# WhatsApp Bulk Messenger

Automate sending bulk messages via WhatsApp Web using Selenium. This script allows you to send the same message to multiple phone numbers automatically.

## Features

- ✅ Automated message sending via WhatsApp Web
- ✅ Human-like typing simulation (random delays between keystrokes)
- ✅ Bulk messaging to multiple contacts
- ✅ Error handling for failed sends
- ✅ Detailed logging of success/failure
- ✅ Random delays between messages to appear more natural
- ✅ Automatic ChromeDriver management

## Prerequisites

1. **Python 3.7 or higher** - [Download Python](https://www.python.org/downloads/)
2. **Google Chrome browser** - [Download Chrome](https://www.google.com/chrome/)
3. **WhatsApp account** with WhatsApp Web access enabled

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or if you prefer using a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Setup

1. **Create a phone numbers file:**
   
   Create a text file (e.g., `phone_numbers.txt`) with one phone number per line. Use international format with country code:
   
   ```
   +1234567890
   +9876543210
   +1122334455
   ```
   
   **Note:** Phone numbers must be in your WhatsApp contacts, or the recipient must have your number saved in their contacts for the message to be sent.

2. **Prepare your message:**
   
   Decide on the message you want to send to all contacts.

## Usage

### Basic Usage

```bash
python whatsapp_bulk_sender.py --numbers phone_numbers.txt --message "Hello, this is a test message!"
```

### Command-Line Arguments

- `-n, --numbers` (required): Path to text file containing phone numbers (one per line)
- `-m, --message` (required): Message to send to all contacts
- `--headless`: Run browser in headless mode (no GUI)
- `--delay-min`: Minimum delay between messages in seconds (default: 2)
- `--delay-max`: Maximum delay between messages in seconds (default: 5)

### Examples

**Send a simple message:**
```bash
python whatsapp_bulk_sender.py -n phone_numbers.txt -m "Hello from automation!"
```

**Send with custom delays:**
```bash
python whatsapp_bulk_sender.py -n phone_numbers.txt -m "Test message" --delay-min 3 --delay-max 7
```

**Run in headless mode:**
```bash
python whatsapp_bulk_sender.py -n phone_numbers.txt -m "Message" --headless
```

## How It Works

1. **Launch Chrome Browser**: The script opens Chrome with WhatsApp Web
2. **QR Code Scan**: You need to scan the QR code with your WhatsApp mobile app
3. **Read Phone Numbers**: Script reads phone numbers from the specified file
4. **Send Messages**: For each number:
   - Searches for the contact in WhatsApp Web
   - Opens the chat
   - Types the message with human-like delays
   - Sends the message
   - Waits before processing the next contact
5. **Summary Report**: Displays success/failure statistics

## Phone Number Format

- Use international format with country code (e.g., `+1234567890`)
- One phone number per line
- Empty lines are ignored
- Phone numbers should match exactly as they appear in WhatsApp

## Troubleshooting

### ChromeDriver Issues

If you encounter ChromeDriver issues, the script uses `webdriver-manager` to automatically download and manage the driver. If problems persist:

1. Make sure Chrome browser is installed and up to date
2. Try updating Selenium: `pip install --upgrade selenium webdriver-manager`

### Contact Not Found

If a contact is not found:
- Ensure the phone number is in international format
- Verify the contact exists in your WhatsApp
- The recipient must have your number saved (for non-contacts)

### QR Code Timeout

If QR code scanning times out:
- Make sure your phone has internet connection
- Try refreshing the page manually
- Restart the script

### Message Not Sending

- Check your internet connection
- Ensure WhatsApp Web is working in your browser
- Verify the message input box is accessible
- Try increasing delays between messages

## Limitations

- WhatsApp may detect automation and temporarily restrict your account
- Phone numbers must be in your contacts or the recipient must have your number
- Rate limiting: Sending too many messages too quickly may trigger restrictions
- WhatsApp Web interface changes may break the script (selectors may need updates)

## Safety Tips

1. **Use Delays**: Don't set delays too low (minimum 2-3 seconds recommended)
2. **Test First**: Test with 1-2 numbers before bulk sending
3. **Respect Limits**: Don't send to hundreds of contacts at once
4. **Monitor Account**: Watch for any warnings from WhatsApp
5. **Use Responsibly**: Only send messages to people who expect them

## Error Handling

The script includes error handling for:
- Invalid phone numbers
- Contacts not found
- Network timeouts
- Browser crashes
- Keyboard interrupts (Ctrl+C)

Failed numbers are logged and the script continues with remaining contacts.

## License

This project is provided as-is for educational purposes. Use responsibly and at your own risk.

## Contributing

If WhatsApp Web interface changes and breaks the script, you may need to update the XPath selectors in `whatsapp_bulk_sender.py`. Common selectors to check:
- Search box: `//div[@contenteditable='true' and @data-tab='3']`
- Message box: `//div[@contenteditable='true' and @data-tab='10']` or `@data-tab='1'`

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify your setup matches the prerequisites
3. Test with a single phone number first

---

**Remember**: Use this tool responsibly and in compliance with WhatsApp's Terms of Service.

