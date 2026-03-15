# Netflix Watcher

Automatically verify your Netflix household on a new device — no manual confirmation required.

## Table of Contents

- [About](#about)
- [How It Works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)

## About

Netflix Watcher automates the household verification process when switching between devices. Instead of manually confirming via email each time, this tool monitors your inbox for Netflix verification emails, automatically clicks the confirmation link, and completes the login process using Selenium.

**Perfect for:** Anyone who frequently switches between TVs or devices and is tired of manual Netflix household verification.

## How It Works

1. You initiate household verification on your TV ("Verify with email")
2. Netflix sends a confirmation email to your registered address
3. Netflix Watcher automatically:
   - Detects the incoming Netflix email
   - Extracts the verification link
   - Opens the link in a browser (Selenium)
   - Logs into your Netflix account
   - Confirms the new device

The entire process takes just seconds.

## Prerequisites

- Docker and Docker Compose (or Make)
- The email address associated with your Netflix account
- Access to incoming emails for that account

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/jakubfrasunek/netflixWatcher
   cd netflixWatcher
   ```

2. Create a `.env` file from the provided `.example.env`:
   ```bash
   cp .example.env .env
   ```

3. Run the application:
   ```bash
   make up
   ```

## Configuration

Edit your `.env` file with the following variables:

| Variable | Description |
|----------|-------------|
| `EMAIL_LOGIN` | The email address associated with your Netflix account |
| `NETFLIX_EMAIL_SENDER` | The sender address for Netflix verification emails (default: `info@account.netflix.com`) |

**Note:** If you forward Netflix emails to a different address, update `NETFLIX_EMAIL_SENDER` to match your email provider's rules.

## Usage

1. Start the application with `make up`
2. Go to Netflix on your TV and select "Verify with email"
3. Watch as Netflix Watcher automatically completes the verification
4. Enjoy your show!