#!/usr/bin/env python3
"""
WhatsApp Bulk Messenger
Automates sending messages to multiple contacts via WhatsApp Web using Selenium.
"""

import argparse
import time
import random
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class WhatsAppBulkSender:
    def __init__(self, headless=False):
        """
        Initialize the WhatsApp Bulk Sender.
        
        Args:
            headless (bool): Run browser in headless mode (default: False)
        """
        self.driver = None
        self.wait = None
        self.headless = headless
        self.results = {
            'success': [],
            'failed': []
        }
    
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options."""
        chrome_options = Options()
        
        # Add user agent to avoid detection
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Disable automation flags
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Keep browser open for debugging (optional)
        if not self.headless:
            chrome_options.add_experimental_option("detach", True)
        
        # Initialize driver with webdriver-manager for automatic driver setup
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Remove webdriver property to avoid detection
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.wait = WebDriverWait(self.driver, 200)
        print("✓ Chrome WebDriver initialized successfully")
    
    def open_whatsapp_web(self):
        """Open WhatsApp Web and wait for QR code scan."""
        print("\nOpening WhatsApp Web...")
        self.driver.get("https://web.whatsapp.com")
        
        print("Waiting for QR code scan...")
        print("Please scan the QR code with your WhatsApp mobile app.")
        
        try:
            # Wait for the main chat interface to load (indicates successful login)
            # Look for the search box or chat list which appears after login
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab='3']"))
            )
            print("✓ QR code scanned successfully! Logged in to WhatsApp Web.")
            time.sleep(2)  # Give it a moment to fully load
            return True
        except TimeoutException:
            print("✗ Timeout: QR code not scanned within 200 seconds.")
            return False
    
    def human_type(self, element, text, min_delay=50, max_delay=150):
        """
        Type text character by character with random delays to simulate human typing.
        
        Args:
            element: Selenium WebElement to type into
            text (str): Text to type
            min_delay (int): Minimum delay between keystrokes in milliseconds
            max_delay (int): Maximum delay between keystrokes in milliseconds
        """
        element.clear()
        for char in text:
            element.send_keys(char)
            # Random delay between keystrokes (convert ms to seconds)
            delay = random.uniform(min_delay / 1000, max_delay / 1000)
            time.sleep(delay)
    
    def search_contact(self, phone_number):
        """
        Search for a contact by phone number.
        
        Args:
            phone_number (str): Phone number to search for
            
        Returns:
            bool: True if contact found, False otherwise
        """
        try:
            # Find the search box (data-tab='3' is the search input)
            search_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab='3']"))
            )
            
            # Clear and search for the phone number
            search_box.click()
            time.sleep(0.5)
            search_box.clear()
            time.sleep(0.3)
            
            # Type phone number
            self.human_type(search_box, phone_number)
            time.sleep(1.5)  # Wait for search results
            
            # Press Enter to select the first search result
            # This works even when contact shows name instead of phone number
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)  # Wait for chat to open
            
            # Verify that chat was opened by checking if message box is available
            # This confirms the contact was found and selected
            try:
                # Check if message input box appears (indicates chat is open)
                self.driver.find_element(
                    By.XPATH,
                    "//div[@contenteditable='true' and (@data-tab='10' or @data-tab='1' or @role='textbox')]"
                )
                return True
            except NoSuchElementException:
                # Chat didn't open, contact might not exist
                # Try to clear search and return False
                try:
                    search_box.clear()
                    time.sleep(0.5)
                    search_box.send_keys(Keys.ESCAPE)  # Close search if possible
                except:
                    pass
                return False
                
        except TimeoutException:
            print(f"  ✗ Timeout while searching for {phone_number}")
            return False
        except Exception as e:
            print(f"  ✗ Error searching for {phone_number}: {str(e)}")
            return False
    
    def send_message(self, phone_number, message):
        """
        Send a message to a contact.
        
        Args:
            phone_number (str): Phone number of the recipient
            message (str): Message to send
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        try:
            # Search for the contact
            if not self.search_contact(phone_number):
                print(f"  ✗ Contact {phone_number} not found")
                return False
            
            # Find the message input box (data-tab='10' or '1' depending on WhatsApp version)
            try:
                message_box = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab='10']"))
                )
            except TimeoutException:
                # Try alternative selector
                try:
                    message_box = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab='1']"))
                    )
                except TimeoutException:
                    # Last resort: find any contenteditable div in the message area
                    message_box = self.driver.find_element(
                        By.XPATH,
                        "//div[@contenteditable='true' and @role='textbox']"
                    )
            
            # Type the message with human-like delays
            message_box.click()
            time.sleep(0.3)
            self.human_type(message_box, message)
            time.sleep(0.5)
            
            # Send the message (press Enter)
            message_box.send_keys(Keys.RETURN)
            time.sleep(1)
            
            print(f"  ✓ Message sent to {phone_number}")
            return True
            
        except TimeoutException:
            print(f"  ✗ Timeout while sending message to {phone_number}")
            return False
        except Exception as e:
            print(f"  ✗ Error sending message to {phone_number}: {str(e)}")
            return False
    
    def send_bulk_messages(self, phone_numbers, message, delay_min=2, delay_max=5):
        """
        Send messages to multiple phone numbers.
        
        Args:
            phone_numbers (list): List of phone numbers
            message (str): Message to send to all contacts
            delay_min (int): Minimum delay between messages in seconds
            delay_max (int): Maximum delay between messages in seconds
        """
        total = len(phone_numbers)
        print(f"\n📱 Starting bulk message sending to {total} contacts...")
        print(f"Message: {message[:50]}{'...' if len(message) > 50 else ''}\n")
        
        for i, phone_number in enumerate(phone_numbers, 1):
            phone_number = phone_number.strip()
            if not phone_number:
                continue
            
            print(f"[{i}/{total}] Processing {phone_number}...")
            
            success = self.send_message(phone_number, message)
            
            if success:
                self.results['success'].append(phone_number)
            else:
                self.results['failed'].append(phone_number)
            
            # Random delay between messages (except for the last one)
            if i < total:
                delay = random.uniform(delay_min, delay_max)
                print(f"  Waiting {delay:.1f} seconds before next message...\n")
                time.sleep(delay)
        
        # Print summary
        print("\n" + "="*50)
        print("📊 SUMMARY")
        print("="*50)
        print(f"✓ Successfully sent: {len(self.results['success'])}")
        print(f"✗ Failed: {len(self.results['failed'])}")
        
        if self.results['failed']:
            print("\nFailed numbers:")
            for number in self.results['failed']:
                print(f"  - {number}")
    
    def cleanup(self):
        """Close the browser and cleanup resources."""
        if self.driver:
            print("\nClosing browser...")
            self.driver.quit()
            print("✓ Cleanup complete")


def read_phone_numbers(file_path):
    """
    Read phone numbers from a text file.
    
    Args:
        file_path (str): Path to the phone numbers file
        
    Returns:
        list: List of phone numbers
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            numbers = [line.strip() for line in f if line.strip()]
        return numbers
    except FileNotFoundError:
        print(f"✗ Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error reading file '{file_path}': {str(e)}")
        sys.exit(1)


def main():
    """Main function to run the WhatsApp bulk sender."""
    parser = argparse.ArgumentParser(
        description='Send bulk messages via WhatsApp Web using automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python whatsapp_bulk_sender.py --numbers phone_numbers.txt --message "Hello!"
  python whatsapp_bulk_sender.py -n numbers.txt -m "Test message" --headless
        """
    )
    
    parser.add_argument(
        '-n', '--numbers',
        required=True,
        help='Path to text file containing phone numbers (one per line)'
    )
    
    parser.add_argument(
        '-m', '--message',
        required=True,
        help='Message to send to all contacts'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode (no GUI)'
    )
    
    parser.add_argument(
        '--delay-min',
        type=int,
        default=2,
        help='Minimum delay between messages in seconds (default: 2)'
    )
    
    parser.add_argument(
        '--delay-max',
        type=int,
        default=5,
        help='Maximum delay between messages in seconds (default: 5)'
    )
    
    args = parser.parse_args()
    
    # Validate phone numbers file exists
    if not Path(args.numbers).exists():
        print(f"✗ Error: Phone numbers file '{args.numbers}' not found.")
        sys.exit(1)
    
    # Read phone numbers
    phone_numbers = read_phone_numbers(args.numbers)
    
    if not phone_numbers:
        print("✗ Error: No phone numbers found in the file.")
        sys.exit(1)
    
    print(f"✓ Loaded {len(phone_numbers)} phone numbers from '{args.numbers}'")
    
    # Initialize sender
    sender = WhatsAppBulkSender(headless=args.headless)
    
    try:
        # Setup and open WhatsApp Web
        sender.setup_driver()
        
        if not sender.open_whatsapp_web():
            print("✗ Failed to login to WhatsApp Web. Exiting.")
            sender.cleanup()
            sys.exit(1)
        
        # Send bulk messages
        sender.send_bulk_messages(
            phone_numbers,
            args.message,
            delay_min=args.delay_min,
            delay_max=args.delay_max
        )
        
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user. Cleaning up...")
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        sender.cleanup()


if __name__ == "__main__":
    main()

