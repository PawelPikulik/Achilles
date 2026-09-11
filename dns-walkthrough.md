# DNS Walkthrough — What Happens When You Type a Website Address

## For a non-technical teammate

---

## The Short Version

When someone types `pawelpikulik.netlify.app` into their browser, four things happen in about 200 milliseconds:

1. **Ask the phone book** — The browser asks a DNS resolver: "What's the IP address for this name?"
2. **Check the records** — The resolver asks the nameserver responsible for `netlify.app`: "Do you have a record for `pawelpikulik`?"
3. **Get the address** — The nameserver replies with an IP address (like `75.2.60.5`).
4. **Make the connection** — The browser connects to that IP address over HTTPS and asks for the website.

That's it. DNS is just a distributed phone book that turns human-readable names into machine-readable addresses.

---

## The Four Players

### 1. The Browser (the client)

This is Chrome, Safari, Firefox, or your phone. It doesn't know any IP addresses by heart. It only knows domain names. Its job is to ask.

### 2. The DNS Resolver (the librarian)

Your internet provider (or Google `8.8.8.8`, or Cloudflare `1.1.1.1`) runs a resolver. Think of it as a librarian who knows which shelf to check. The resolver doesn't own the phone book — it knows how to find the right one.

**What the resolver does:**
- Receives the query: "What's the IP for `pawelpikulik.netlify.app`?"
- Checks its own cache first ("Did someone ask this recently?").
- If not cached, asks the root nameserver: "Who manages `.app`?"
- The root replies: "Ask the `.app` nameserver."
- The resolver asks the `.app` nameserver: "Who manages `netlify.app`?"
- The `.app` nameserver replies: "Here's the nameserver for `netlify.app`."
- The resolver asks the `netlify.app` nameserver: "What's the IP for `pawelpikulik`?"
- Gets the IP, caches it, and sends it back to the browser.

This sounds like a lot, but it usually happens in under 100ms because of caching at every level.

### 3. The Nameserver (the owner of the record)

Netlify runs the nameservers for `netlify.app`. They hold the actual records — the lines in the phone book. When you deploy a site to Netlify, Netlify automatically creates an **A record** (or **CNAME record**) that maps your site name to the server IP where your files live.

### 4. The Web Server (the host)

This is Netlify's server at the IP address the nameserver returned. It receives the HTTPS request, serves the files (`index.html`, `styles.css`), and the browser renders the page.

---

## What Is a CNAME Record?

A **CNAME** (Canonical Name) record is a redirect at the DNS level. It says: "This name is just an alias for another name."

**Example:**

```
www.pawelpikulik.netlify.app  CNAME  pawelpikulik.netlify.app
```

When someone asks for `www.pawelpikulik.netlify.app`, the nameserver doesn't give an IP. It says: "Go ask about `pawelpikulik.netlify.app` instead." The resolver then repeats the lookup for the canonical name and gets the actual IP.

**When to use CNAME:**
- Pointing `www` to the root domain
- Pointing a custom domain (like `pawelpikulik.com`) to a Netlify site
- Any time you want one name to resolve through another

**When NOT to use CNAME:**
- At the root domain (`pawelpikulik.com` with no `www`) — DNS doesn't allow CNAME at the root. Use an A record or ALIAS record instead.

---

## The Full Journey: Step by Step

Let's trace what happens when someone types `pawelpikulik.netlify.app` and presses Enter.

**Step 0 — Typing:**
The user types `pawelpikulik.netlify.app` into the browser address bar.

**Step 1 — Browser cache check:**
The browser checks: "Did I visit this site recently? Do I still have the IP in memory?" If yes, skip to Step 6. If no, continue.

**Step 2 — OS cache check:**
The browser asks the operating system: "Do you have this in your DNS cache?" The OS might. If yes, return it. If no, continue.

**Step 3 — Ask the resolver:**
The OS sends a DNS query to the configured resolver (usually your ISP's resolver, or a public one like Cloudflare `1.1.1.1`).

**Step 4 — Resolver does the walking:**
The resolver doesn't know the answer, but it knows who to ask:
1. Asks a **root nameserver** (there are 13 logical root servers worldwide): "Who runs `.app`?"
2. Root replies: "Ask these nameservers for `.app`."
3. Resolver asks a **TLD nameserver** (Top-Level Domain, runs `.app`): "Who runs `netlify.app`?"
4. TLD replies: "Here are the nameservers for `netlify.app`."
5. Resolver asks the **authoritative nameserver** (Netlify's server): "What's the record for `pawelpikulik`?"
6. Authoritative nameserver replies: "The A record is `75.2.60.5`" (or a CNAME that points to another name).

**Step 5 — Resolver caches and replies:**
The resolver stores the answer in its cache (so the next person asking doesn't require all these steps) and sends the IP back to the OS, which passes it to the browser.

**Step 6 — Browser connects:**
The browser opens a TCP connection to `75.2.60.5` on port 443 (HTTPS).

**Step 7 — TLS handshake:**
The browser and server agree on encryption. Netlify's server presents an SSL certificate for `pawelpikulik.netlify.app`. The browser verifies it (signed by a trusted Certificate Authority). The padlock appears.

**Step 8 — HTTP request:**
The browser sends: `GET / HTTP/1.1` with `Host: pawelpikulik.netlify.app`.

**Step 9 — Server responds:**
Netlify serves `index.html` (and later `styles.css` when the browser requests it).

**Step 10 — Page renders:**
The browser parses HTML, fetches CSS, and renders the page. Total time from typing to seeing content: usually 200–500ms.

---

## Why This Matters for This Site

Netlify handles almost all of this automatically:
- **Nameservers:** Netlify runs the authoritative nameservers for `netlify.app`.
- **Records:** When I deploy and rename the site to `pawelpikulik`, Netlify creates the DNS record automatically.
- **HTTPS:** Netlify provisions and renews the SSL certificate automatically (via Let's Encrypt).
- **Caching:** DNS responses are cached at the browser, OS, resolver, and CDN levels.

The only thing I configure manually is the **site name** in Netlify's UI. The DNS record is created automatically. If I ever connect a custom domain (like `pawelpikulik.com`), I would add a **CNAME record** in my domain registrar's DNS panel pointing to `pawelpikulik.netlify.app`, and Netlify would serve the same site with a certificate for the custom domain.

---

## One-Sentence Summary

**DNS is a distributed phone book that turns human-readable domain names into IP addresses, and a CNAME record is an alias that says "ask this other name instead."**
