# WhatsApp Setup Instructions

## Step 1: Start WhatsApp Pairing (Run on VM)

```bash
ssh ai
clawdbot configure --section channels
# Select WhatsApp when prompted
# Choose "Link with QR code"
```

## Step 2: Scan QR Code (On Your Phone)

1. Open WhatsApp on your phone
2. Tap Menu (⋮) > Linked Devices
3. Tap "Link a Device"
4. Scan the QR code displayed in the terminal

## Step 3: Verify Connection

Once scanned, Clawdbot will show "Connected!" and you can send messages.

## Test Command

Send this message from WhatsApp to test:
```
Check my email
```

Expected response: Gmail skill executes and returns email count.

---

## Alternative: Google Chat Setup

If WhatsApp pairing is difficult via SSH, you can use Google Chat instead:

1. Enable Matrix plugin: `clawdbot plugins enable matrix`
2. Restart gateway: `systemctl --user restart clawdbot-gateway`
3. Configure Matrix bridge to Google Chat
4. Invite Clawdbot to a Google Chat space

