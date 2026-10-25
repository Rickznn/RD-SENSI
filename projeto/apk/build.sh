#!/bin/bash
set -e
cd "$(dirname "$0")"
: "${KS_PASS:?Defina KS_PASS com a senha da keystore}"
SDK=$HOME/android-sdk; BT=$SDK/build-tools/34.0.0; JAR=$SDK/platforms/android-34/android.jar
rm -rf build && mkdir -p build/res build/classes build/dex
cp ../index.html assets/index.html
$BT/aapt2 compile --dir res -o build/res/
$BT/aapt2 link -I $JAR --manifest AndroidManifest.xml -A assets -o build/unsigned.apk build/res/*.flat --java build/gen
javac -source 8 -target 8 -bootclasspath $JAR -classpath $JAR -d build/classes $(find src build/gen -name '*.java') 2>&1 | grep -v "warning" || true
$BT/d8 --release --lib $JAR --min-api 21 --output build/dex $(find build/classes -name '*.class')
cp build/unsigned.apk build/withdex.apk
(cd build/dex && zip -q ../withdex.apk classes.dex)
$BT/zipalign -f -p 4 build/withdex.apk build/aligned.apk
[ -f rdsensi.keystore ] || keytool -genkeypair -keystore rdsensi.keystore -alias rdsensi -keyalg RSA -keysize 2048 -validity 10000 -storepass $KS_PASS -keypass $KS_PASS -dname "CN=RD SENSI, O=RD SENSI, C=BR" >/dev/null 2>&1
$BT/apksigner sign --ks rdsensi.keystore --ks-pass pass:$KS_PASS --key-pass pass:$KS_PASS --out ../RD-SENSI.apk build/aligned.apk
$BT/apksigner verify ../RD-SENSI.apk && echo "APK OK: $(du -h ../RD-SENSI.apk | cut -f1)"
