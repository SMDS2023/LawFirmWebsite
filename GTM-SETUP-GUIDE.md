# Google Tag Manager Setup Guide
## Migrating Google Analytics 4 and Microsoft Clarity to GTM

This guide will help you complete the migration to Google Tag Manager (GTM) best practices by configuring your Google Analytics 4 and Microsoft Clarity tags within GTM.

## Current Status

✅ **Google Tag Manager** (`GTM-PLX85K8L`) - Installed on all 40 HTML pages
⚠️ **Google Analytics 4** (`G-D28BZM9QDC`) - Currently hardcoded in HTML (will move to GTM)
⚠️ **Microsoft Clarity** (`reu4dibx4h`) - Currently hardcoded in HTML (will move to GTM)

## Step 1: Configure Google Analytics 4 in GTM

### 1.1 Access Google Tag Manager
1. Go to https://tagmanager.google.com/
2. Select your container (`GTM-PLX85K8L`)

### 1.2 Create GA4 Configuration Tag
1. Click **Tags** in the left sidebar
2. Click **New** button
3. Click on the tag configuration area
4. Select **Google Analytics: GA4 Configuration**
5. Enter your Measurement ID: `G-D28BZM9QDC`
6. Under **Triggering**, click the trigger area
7. Select **All Pages** trigger
8. Name the tag: `GA4 - Configuration`
9. Click **Save**

### 1.3 Verify GA4 Tag (Optional but Recommended)
1. Click **Preview** in the top right
2. Enter your website URL
3. Navigate through a few pages
4. In Tag Assistant, verify the GA4 Configuration tag fires on all pages
5. Exit preview mode

## Step 2: Configure Microsoft Clarity in GTM

### 2.1 Create Custom HTML Tag for Clarity
1. In GTM, click **Tags** → **New**
2. Click on the tag configuration area
3. Select **Custom HTML**
4. Paste the following code:

```html
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "reu4dibx4h");
</script>
```

5. Check the box for **Support document.write**
6. Under **Triggering**, select **All Pages**
7. Name the tag: `Microsoft Clarity`
8. Click **Save**

## Step 3: Publish Your Container

1. Click **Submit** in the top right corner
2. Add a Version Name: `GA4 and Clarity Migration`
3. Add a Description: `Migrated Google Analytics 4 and Microsoft Clarity tags from hardcoded HTML to GTM`
4. Click **Publish**

## Step 4: Test Your Implementation

### 4.1 Test GA4
1. Open your website in an incognito/private browser window
2. Open browser DevTools (F12)
3. Go to the **Network** tab
4. Filter by `google-analytics` or `gtag`
5. Navigate to a few pages
6. Verify you see requests to `www.google-analytics.com/g/collect`

**Alternative:** Use Google Analytics DebugView
1. Install Google Analytics Debugger extension
2. Visit your site
3. Check GA4 DebugView in Google Analytics admin for real-time events

### 4.2 Test Microsoft Clarity
1. Go to https://clarity.microsoft.com/
2. Select your project
3. Look for recent sessions appearing
4. Click on a session to watch the recording

**Alternative:** Check Network Tab
1. Open DevTools → Network tab
2. Filter by `clarity.ms`
3. Verify you see requests to `https://www.clarity.ms/`

### 4.3 Test GTM Container
1. Open your website
2. Open DevTools → Console
3. Type: `google_tag_manager['GTM-PLX85K8L'].dataLayer.get('gtm.start')`
4. You should see a timestamp, confirming GTM loaded successfully

## Step 5: Remove Hardcoded Scripts (After Testing)

**IMPORTANT:** Only proceed after confirming tags work correctly in GTM!

Once you've verified that both Google Analytics and Microsoft Clarity are working through GTM:

1. Notify me that testing is complete
2. I will remove the hardcoded GA4 and Clarity scripts from all HTML files
3. This will leave only GTM scripts in your HTML (cleaner, more maintainable)

## Benefits of This Setup

✅ **Centralized Management** - All tags managed in one place
✅ **No Code Changes** - Add/remove tags without touching HTML
✅ **Better Performance** - Async loading and optimized delivery
✅ **Tag Sequencing** - Control firing order and dependencies
✅ **Built-in Debugging** - GTM Preview mode for troubleshooting
✅ **Version Control** - Roll back tag changes if needed
✅ **Collaboration** - Multiple team members can manage tags

## Additional Configuration Options (Optional)

### Enhanced Event Tracking
Once comfortable with GTM, you can add:
- Form submission tracking
- Click tracking (phone, email, CTA buttons)
- Scroll depth tracking
- PDF download tracking
- Outbound link tracking

### Advanced GA4 Features
- Custom events
- User properties
- Enhanced ecommerce (if applicable)
- Cross-domain tracking

## Troubleshooting

### GA4 Not Firing
- Check Measurement ID is correct: `G-D28BZM9QDC`
- Verify trigger is set to "All Pages"
- Check for JavaScript errors in Console

### Clarity Not Recording
- Verify Project ID is correct: `reu4dibx4h`
- Check that Custom HTML tag has "Support document.write" checked
- Wait 5-10 minutes for first session to appear

### GTM Not Loading
- Check browser console for errors
- Verify GTM container ID: `GTM-PLX85K8L`
- Clear browser cache and test in incognito mode

## Next Steps

1. Complete Steps 1-4 above
2. Test thoroughly for 24-48 hours
3. Confirm both GA4 and Clarity are collecting data properly
4. Let me know when ready to remove hardcoded scripts
5. I'll complete the cleanup and push final changes

## Support Resources

- **GTM Documentation:** https://support.google.com/tagmanager
- **GA4 Setup Guide:** https://support.google.com/analytics/answer/9304153
- **Clarity Documentation:** https://learn.microsoft.com/en-us/clarity/

---

**Questions?** Let me know if you need help with any of these steps!
