# ServiceMatchup Website

Multi-page home services lead generation website built with static HTML/CSS.

## Pages

| Page | File | URL |
|------|------|-----|
| Homepage | `index.html` | `/` |
| Roofing | `roofing.html` | `/roofing` |
| HVAC | `hvac.html` | `/hvac` |
| Plumbing | `plumbing.html` | `/plumbing` |
| Electrical | `electrical.html` | `/electrical` |
| Solar | `solar.html` | `/solar` |
| Windows & Siding | `windows.html` | `/windows` |

## Setup: LeadCapture.io Form

All CTA buttons link to `#` by default. To connect your LeadCapture.io form:

1. Get your form URL from LeadCapture.io (e.g., `https://form.leadcapture.io/your-form-id`)
2. Find and replace all `href="#"` on CTA buttons with your form URL
3. Or embed the form on a dedicated page and link to it

## Deploy to GitHub + Cloudflare Pages

### Step 1: Create GitHub Repository

```bash
# Navigate to this folder
cd servicematchup

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - ServiceMatchup website"

# Create repo on GitHub (go to github.com/new)
# Name it: servicematchup

# Connect and push
git remote add origin https://github.com/YOUR_USERNAME/servicematchup.git
git branch -M main
git push -u origin main
```

### Step 2: Connect Cloudflare Pages

1. Go to [dash.cloudflare.com](https://dash.cloudflare.com)
2. Click **Workers & Pages** in the sidebar
3. Click **Create application** → **Pages** → **Connect to Git**
4. Select your `servicematchup` repository
5. Configure build settings:
   - **Build command:** (leave empty — no build step needed)
   - **Build output directory:** `/` (root)
6. Click **Save and Deploy**

Your site will be live at `servicematchup.pages.dev` within 60 seconds.

### Step 3: Add Custom Domain

1. In Cloudflare Pages, go to your project → **Custom domains**
2. Click **Set up a custom domain**
3. Enter `servicematchup.com` (or your domain)
4. If your domain is on Cloudflare DNS, it auto-configures
5. If not, add the CNAME record Cloudflare provides to your DNS

### Step 4: Add Facebook Pixel

Add this before `</head>` in every HTML file:

```html
<!-- Facebook Pixel -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'YOUR_PIXEL_ID');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=YOUR_PIXEL_ID&ev=PageView&noscript=1"/></noscript>
```

Replace `YOUR_PIXEL_ID` with your actual Facebook Pixel ID.

## File Structure

```
servicematchup/
├── index.html          # Homepage
├── roofing.html        # Roofing vertical page
├── hvac.html           # HVAC vertical page
├── plumbing.html       # Plumbing vertical page
├── electrical.html     # Electrical vertical page
├── solar.html          # Solar vertical page
├── windows.html        # Windows & Siding vertical page
├── styles.css          # Shared stylesheet
└── README.md           # This file
```

## Making Changes

Edit the HTML files directly. Push to GitHub and Cloudflare Pages auto-deploys:

```bash
git add .
git commit -m "Updated hero copy"
git push
```

Cloudflare Pages rebuilds automatically in ~30 seconds.
