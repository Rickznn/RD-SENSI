package com.rd.sensi;

import android.app.Activity;
import android.app.ActivityManager;
import android.content.IntentFilter;
import android.content.pm.ResolveInfo;
import android.os.BatteryManager;
import android.os.Build;
import android.provider.Settings;
import org.json.JSONObject;
import java.util.HashSet;
import java.util.List;
import android.content.ActivityNotFoundException;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.webkit.ConsoleMessage;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    private WebView web;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        web = new WebView(this);
        web.setBackgroundColor(0xFF0B0D12);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setSupportMultipleWindows(false);
        web.addJavascriptInterface(new Bridge(), "AndroidApp");
        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest req) {
                return handle(req.getUrl().toString());
            }
            @SuppressWarnings("deprecation")
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return handle(url);
            }
        });
        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onConsoleMessage(ConsoleMessage m) {
                Log.d("RDSENSI", m.message() + " @" + m.lineNumber());
                return true;
            }
        });
        setContentView(web);
        web.loadUrl("file:///android_asset/index.html");
    }

    private boolean handle(String url) {
        if (url.startsWith("file:")) return false;
        if (url.startsWith("intent:")) {
            try {
                Intent parsed = Intent.parseUri(url, Intent.URI_INTENT_SCHEME);
                String pkg = parsed.getPackage();
                Intent launch = pkg == null ? null : getPackageManager().getLaunchIntentForPackage(pkg);
                if (launch != null) {
                    startActivity(launch);
                } else if (pkg != null) {
                    openStore(pkg);
                }
            } catch (Exception ignored) { }
            return true;
        }
        openExternal(url);
        return true;
    }

    private void openStore(String pkg) {
        try {
            startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse("market://details?id=" + pkg)));
        } catch (ActivityNotFoundException e) {
            openExternal("https://play.google.com/store/apps/details?id=" + pkg);
        }
    }

    private void openExternal(String url) {
        try {
            startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
        } catch (Exception ignored) { }
    }

    @Override
    public void onBackPressed() {
        if (web.canGoBack()) web.goBack(); else super.onBackPressed();
    }

    private class Bridge {
        @JavascriptInterface
        public void copy(String text) {
            ClipboardManager cm = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
            cm.setPrimaryClip(ClipData.newPlainText("RD SENSI", text));
        }

        @JavascriptInterface
        public void share(String text) {
            Intent i = new Intent(Intent.ACTION_SEND);
            i.setType("text/plain");
            i.putExtra(Intent.EXTRA_TEXT, text);
            startActivity(Intent.createChooser(i, "Compartilhar sensi"));
        }
        @JavascriptInterface
        public String deviceInfo() {
            JSONObject o = new JSONObject();
            try {
                ActivityManager am = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
                ActivityManager.MemoryInfo mi = new ActivityManager.MemoryInfo();
                am.getMemoryInfo(mi);
                o.put("manufacturer", Build.MANUFACTURER);
                o.put("brand", Build.BRAND);
                o.put("model", Build.MODEL);
                o.put("android", Build.VERSION.RELEASE);
                o.put("ramTotal", mi.totalMem / 1048576L);
                o.put("ramAvail", mi.availMem / 1048576L);
                Intent b = registerReceiver(null, new IntentFilter(Intent.ACTION_BATTERY_CHANGED));
                if (b != null) {
                    int level = b.getIntExtra(BatteryManager.EXTRA_LEVEL, -1);
                    int scale = b.getIntExtra(BatteryManager.EXTRA_SCALE, 100);
                    int status = b.getIntExtra(BatteryManager.EXTRA_STATUS, -1);
                    o.put("battery", level * 100 / Math.max(scale, 1));
                    o.put("temp", b.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, 0) / 10.0);
                    o.put("charging", status == BatteryManager.BATTERY_STATUS_CHARGING || status == BatteryManager.BATTERY_STATUS_FULL);
                }
            } catch (Exception ignored) { }
            return o.toString();
        }

        @JavascriptInterface
        public String boost() {
            JSONObject o = new JSONObject();
            try {
                ActivityManager am = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
                ActivityManager.MemoryInfo mi = new ActivityManager.MemoryInfo();
                am.getMemoryInfo(mi);
                long before = mi.availMem;
                Intent q = new Intent(Intent.ACTION_MAIN);
                q.addCategory(Intent.CATEGORY_LAUNCHER);
                List<ResolveInfo> apps = getPackageManager().queryIntentActivities(q, 0);
                HashSet<String> seen = new HashSet<String>();
                for (ResolveInfo ri : apps) {
                    String pkg = ri.activityInfo.packageName;
                    if (pkg.equals(getPackageName()) || !seen.add(pkg)) continue;
                    am.killBackgroundProcesses(pkg);
                }
                System.gc();
                Thread.sleep(800);
                am.getMemoryInfo(mi);
                o.put("before", before / 1048576L);
                o.put("after", mi.availMem / 1048576L);
                o.put("apps", seen.size());
            } catch (Exception ignored) { }
            return o.toString();
        }

        @JavascriptInterface
        public void openSettings(final String key) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    Intent i;
                    if ("display".equals(key)) i = new Intent(Settings.ACTION_DISPLAY_SETTINGS);
                    else if ("battery".equals(key)) i = new Intent(Settings.ACTION_BATTERY_SAVER_SETTINGS);
                    else if ("dev".equals(key)) i = new Intent(Settings.ACTION_APPLICATION_DEVELOPMENT_SETTINGS);
                    else if ("storage".equals(key)) i = new Intent(Settings.ACTION_INTERNAL_STORAGE_SETTINGS);
                    else if ("wifi".equals(key)) i = new Intent(Settings.ACTION_WIFI_SETTINGS);
                    else if ("ff".equals(key)) {
                        String pkg = null;
                        if (getPackageManager().getLaunchIntentForPackage("com.dts.freefireth") != null) pkg = "com.dts.freefireth";
                        else if (getPackageManager().getLaunchIntentForPackage("com.dts.freefiremax") != null) pkg = "com.dts.freefiremax";
                        i = pkg != null
                            ? new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:" + pkg))
                            : new Intent(Settings.ACTION_APPLICATION_SETTINGS);
                    }
                    else i = new Intent(Settings.ACTION_SETTINGS);
                    i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    try {
                        startActivity(i);
                    } catch (Exception e) {
                        try { startActivity(new Intent(Settings.ACTION_SETTINGS).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)); } catch (Exception ignored) { }
                    }
                }
            });
        }
    }
}
