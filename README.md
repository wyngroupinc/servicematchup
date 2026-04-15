# ServiceMatchup Website

## Your URLs

| URL | Page | Purpose |
|-----|------|---------|
| servicematchup.com | Homepage | General home services overview |
| servicematchup.com/roof-inspection | Roofing Landing Page | Facebook ads point HERE |
| servicematchup.com/get-started | Form Page | Landing page CTAs point HERE |
| servicematchup.com/roofing | Roofing vertical page | From site navigation |
| servicematchup.com/hvac | HVAC vertical page | From site navigation |
| servicematchup.com/plumbing | Plumbing vertical page | From site navigation |
| servicematchup.com/electrical | Electrical vertical page | From site navigation |
| servicematchup.com/solar | Solar vertical page | From site navigation |
| servicematchup.com/windows | Windows & Siding vertical page | From site navigation |

## Facebook Ad Flow

```
Facebook Ad → servicematchup.com/roof-inspection → servicematchup.com/get-started → Lead Captured
```

## File Structure

```
servicematchup/
├── index.html              # Homepage
├── roof-inspection.html    # Facebook roofing landing page
├── get-started.html        # Form page (LeadCapture.io embed)
├── roofing.html            # Roofing vertical page
├── hvac.html               # HVAC vertical page
├── plumbing.html           # Plumbing vertical page
├── electrical.html         # Electrical vertical page
├── solar.html              # Solar vertical page
├── windows.html            # Windows & Siding vertical page
├── styles.css              # Shared stylesheet
└── README.md               # This file
```

## How to Deploy / Re-deploy

### First time setup:
1. Go to github.com/new → create repo called "servicematchup"
2. Upload ALL files from this folder
3. Go to Cloudflare → Workers & Pages → Create → Pages → Connect to Git
4. Select your repo, leave build command empty, output directory: /
5. Deploy

### To update your site:
1. Go to your repo on github.com
2. Click "Add file" → "Upload files"
3. Drag ALL files in (it will overwrite the old ones)
4. Click "Commit changes"
5. Cloudflare auto-deploys in ~30 seconds

### IMPORTANT: Upload ALL files every time
If you only upload some files, the others won't update. Always upload the complete set.
