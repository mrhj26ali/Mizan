# view_reports.py
import os, json, glob

out_path = "reports_summary.txt"
# Find all JSON files in the mizan_reports folder and sort them by timestamp
files = sorted(glob.glob("reports/*.json"))

if not files:
    print("❌ لم يتم العثور على أي تقارير في مجلد mizan_reports/")
else:
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"📊 Mizan Reports Summary ({len(files)} files)\n" + "="*50 + "\n\n")
        
        for file in files:
            f.write(f"📄 File: {os.path.basename(file)}\n" + "-"*40 + "\n")
            try:
                with open(file, "r", encoding="utf-8") as rf:
                    data = json.load(rf)
                    # indent=4 makes it pretty, ensure_ascii=False keeps Arabic readable
                    f.write(json.dumps(data, indent=4, ensure_ascii=False) + "\n\n")
            except Exception as e:
                f.write(f"❌ Error reading file: {e}\n\n")

    print(f"✅ تم تجميع {len(files)} تقرير بنجاح!")
    print(f"👈 افتح الملف التالي لمشاهدة النتائج: {out_path}")