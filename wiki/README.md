# 📝 Wiki Upload Instructions

I've created comprehensive wiki documentation for AI Nexus! Here's how to publish it to GitHub.

## 📋 What's Included

The `wiki/` directory contains:
- **Home.md** - Welcome page
- **Installation-Guide.md** - Quick start guide
- **User-Guide.md** - Feature documentation
- **Mobile-App-Setup.md** - Mobile connection guide
- **Troubleshooting.md** - Common issues and solutions
- **API-Documentation.md** - Developer reference

## 🚀 How to Publish

### Option 1: GitHub Web Interface (Easiest)

1. **Enable Wiki**:
   - Go to your GitHub repo: https://github.com/jimmymannekkattu/Multi-LLM-Aggregator
   - Click **Settings** tab
   - Scroll to **Features** section
   - Check ☑️ **Wikis**

2. **Create Pages**:
   - Click **Wiki** tab (appears after enabling)
   - Click **Create the first page**
   - Copy content from `wiki/Home.md`
   - Click **Save Page**

3. **Add Remaining Pages**:
   - Click **New Page**
   - Set title as filename (e.g., "Installation-Guide")
   - Copy content from corresponding `.md` file
   - Repeat for all files

### Option 2: Git Clone (Advanced)

```bash
# Clone the wiki repository
git clone https://github.com/jimmymannekkattu/Multi-LLM-Aggregator.wiki.git

# Copy wiki files
cp wiki/*.md Multi-LLM-Aggregator.wiki/

# Commit and push
cd Multi-LLM-Aggregator.wiki
git add .
git commit -m "Add comprehensive wiki documentation"
git push origin master
```

## ✅ Verify

After publishing, visit:
https://github.com/jimmymannekkattu/Multi-LLM-Aggregator/wiki

You should see:
- Home page with navigation
- All guides accessible via sidebar
- Properly formatted markdown

## 📌 Tips

- **Navigation**: GitHub auto-generates sidebar from page names
- **Links**: I've used `(Page-Name)` format for internal links
- **Images**: To add images, upload to wiki or use external URLs
- **Editing**: Anyone can edit if Wiki is public (configurable in settings)

---

That's it! Your wiki is ready to help users. 🎉
