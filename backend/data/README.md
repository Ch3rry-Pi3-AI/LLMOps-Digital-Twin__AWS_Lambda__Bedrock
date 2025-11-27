# 📁 **`/backend/data` — Personal Data Files**

The `data` directory contains structured and unstructured personal information used to enhance the behaviour of the Digital Twin. These files help the backend provide richer, more personalised responses by supplying background facts, experience summaries, and communication style preferences.

## Files Inside This Folder

### **1. `facts.json`**

A machine-readable summary of key personal details such as full name, location, LinkedIn profile, professional specialties, and academic history.
Used by the backend to provide accurate factual information when the Digital Twin is asked about your background.

### **2. `summary.txt`**

A natural-language overview of your professional profile, including your role, expertise, experience level, and current focus areas.
This helps the Digital Twin answer questions about your career, interests, and ongoing projects in a personalised and consistent manner.

### **3. `style.txt`**

Describes your preferred communication style.
This guides the Digital Twin in matching your tone—professional but approachable, clear, concise, and practical.

### **4. `LinkedIn.pdf`**

A PDF version of your professional CV.
While not directly parsed by the Digital Twin, it serves as a reference document containing your full work history, skills, and achievements. This file can be used for future enhancements such as automated CV extraction or deeper profile modelling.