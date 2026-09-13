# What a Backend Is, What My Feature Does, and How the Data Flows

## A plain-words explainer for a non-technical teammate

---

## What a Backend Is

A **backend** is the part of a website you do not see. It lives on a server somewhere on the internet — not on your phone or laptop. Its job is to receive data, process it, store it, and send back a response.

Think of a restaurant. The frontend is the dining room: the menu, the table, the decor. The backend is the kitchen: the cooks, the recipes, the ingredients, the dishwasher. You don't see the kitchen, but without it, the dining room is just an empty room with nice chairs.

On a website, the frontend is the HTML, CSS, and JavaScript that renders in your browser. The backend is the server that:
- Receives your contact form submission
- Stores it in a database or forwards it to an email inbox
- Sends back a confirmation: "Message received"

The frontend and backend talk to each other over **HTTP** — the same protocol your browser uses to load a page, but in this case the browser *sends* data instead of just *receiving* it.

---

## What My Feature Does

My personal website has a **working contact form** on the page. A visitor can type their name, email, and message, click "Send message," and the message actually reaches me. It is not a fake button. It is not a `mailto:` link that opens your email client. It is a real form submission that travels across the internet, is validated, stored, and forwarded to my inbox.

**Why this feature:** A portfolio that just displays text is a poster. A portfolio that lets someone reach you is a tool. For a Head of AI evaluating whether I can ship end-to-end products, a genuinely working contact form is the smallest possible proof that I understand the full loop: user action → data transmission → server processing → real-world result.

---

## How the Data Flows — Step by Step

Here is exactly what happens when someone fills out the form and clicks "Send message."

### Step 1 — The Visitor Fills the Form

The visitor is on `https://pawelpikulik.netlify.app`. They see the contact form with three fields: Name, Email, Message. They type their information and click the "Send message" button.

### Step 2 — The Browser Intercepts the Click

Normally, a form submission would reload the entire page. That is a bad user experience. My JavaScript intercepts the click with `event.preventDefault()`. The page stays exactly where it is. A small text line appears below the button: "Sending..."

### Step 3 — The Browser Packages the Data

JavaScript reads the values from the three form fields, bundles them into a `FormData` object (a standard web format for sending form data), and prepares an HTTP **POST** request.

### Step 4 — The Browser Sends the Data to the Backend

The browser sends a POST request to `https://formspree.io/f/mgvalvjr`.

**Formspree** is a managed backend service. I did not write the backend myself — I do not run a server, manage a database, or configure email SMTP. Formspree handles all of that. This is a deliberate choice: for a single contact form on a static portfolio, running my own backend (like a FastAPI server on Render or Railway) would add hosting cost, cold-start latency, and maintenance overhead. Formspree is free for up to 50 submissions per month, which is more than enough for a portfolio.

The POST request includes:
- `name`: the visitor's name
- `email`: the visitor's email address
- `message`: the visitor's message
- `Accept: application/json` header so the server knows to reply with JSON

### Step 5 — The Backend Receives and Validates the Data

Formspree's server receives the POST request. It checks:
- Are all required fields present?
- Is the email address formatted like an email?
- Is this a duplicate submission or spam? (basic rate limiting)

If validation passes, Formspree stores the submission in its database and queues an email notification.

### Step 6 — The Backend Sends a Response

Formspree sends back an HTTP response with status `200 OK` and a JSON body:

```json
{
  "ok": true,
  "next": "https://formspree.io/thanks?language=en"
}
```

### Step 7 — The Frontend Shows Confirmation

My JavaScript receives the `200 OK` response, reads the JSON, and updates the status text below the button:

> "Message sent. I will be in touch shortly."

The form also clears itself so the visitor knows the action is complete.

If something went wrong — network error, Formspree down, validation failure — the JavaScript catches the error and shows:

> "Something went wrong. Please try again."

### Step 8 — I Receive the Message

Separately from the browser conversation, Formspree forwards the submission to my email inbox (`pawel.pikulik@velans.com`). I see the visitor's name, email, and message in my email. I can reply directly.

---

## The Full Data Flow Diagram

```
Visitor (browser)
    │
    │ Types name, email, message
    │ Clicks "Send message"
    │
    ▼
JavaScript (frontend)
    │
    │ Intercepts click
    │ Packages data into FormData
    │
    ▼
HTTP POST request
    │
    │ Travels over the internet to formspree.io
    │
    ▼
Formspree backend (server)
    │
    │ Validates fields
    │ Stores submission
    │ Queues email to pawel.pikulik@velans.com
    │
    ▼
HTTP 200 OK response (JSON)
    │
    │ Travels back to the browser
    │
    ▼
JavaScript (frontend)
    │
    │ Reads JSON
    │ Updates status text: "Message sent..."
    │ Clears form fields
    │
    ▼
Visitor sees confirmation

(Parallel)
Formspree email queue
    │
    ▼
Email arrives in my inbox
```

---

## Why Formspree and Not My Own Backend

I built my own backend for Achilles (FastAPI + JSON memory). For the contact form, I chose a managed service instead. Here is the honest tradeoff:

| Factor | Own Backend (FastAPI on Render) | Managed Service (Formspree) |
|--------|--------------------------------|----------------------------|
| **Cost** | Free tier exists but sleeps after inactivity; first request is slow (5–10s cold start) | Free tier, always warm |
| **Maintenance** | I must keep the server running, handle errors, monitor uptime | Zero maintenance |
| **Email delivery** | I must configure SMTP, handle bounces, avoid spam filters | Formspree handles deliverability |
| **Spam protection** | I must build rate limiting, CAPTCHA, or honeypot | Built-in basic protection |
| **Complexity** | More impressive technically | Simpler, more reliable for one form |
| **Portfolio signal** | Shows I *can* build backends | Shows I *choose* the right tool for the job |

I chose Formspree because the assignment asks for a working feature, not a backend showcase. The right tool for a single contact form is a managed form backend. My FastAPI backend is already demonstrated in the Achilles project.

---

## What I Would Do at Scale

If this portfolio received 100+ messages per month, or if I needed custom logic (auto-replies, CRM integration, file attachments), I would replace Formspree with:

1. **A FastAPI backend** on Render or Railway (the same stack as Achilles)
2. **A SQLite or PostgreSQL database** to store submissions with timestamps
3. **An email service** like SendGrid or AWS SES for reliable delivery
4. **Rate limiting and honeypot fields** for spam protection

The current architecture is a deliberate, honest MVP. It works, it is free, and it requires zero maintenance. That is the point.

---

## One-Sentence Summary

**The contact form on my portfolio is a real, working feature: when a visitor submits it, JavaScript intercepts the click, sends the data via HTTP POST to Formspree's managed backend, which validates and stores the submission and forwards it to my email — all without reloading the page, and all on a free tier.**
