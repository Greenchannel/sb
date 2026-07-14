# Keep WebView classes
-keepclassmembers class * extends android.webkit.WebView {
    public void onPageStarted(android.webkit.WebView, java.lang.String, android.graphics.Bitmap);
    public void onPageFinished(android.webkit.WebView, java.lang.String);
    public boolean shouldOverrideUrlLoading(android.webkit.WebView, android.webkit.WebResourceRequest);
}