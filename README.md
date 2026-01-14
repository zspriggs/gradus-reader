## Juno
A web-based reading environment for ancient Greek and Latin texts, designed to help learners develop morphological skills through annotations and instant feedback.

### Overview
By integrating treebank data, Juno enables students to make their own attempts at text annotation, while providing the scaffolding to correct errors.  

### Features
**Currently Available**
- *Interactive Morphology Checking*: Click any word to test your understanding of its case, number, gender, tense, mood, or voice, with instant feedback
- *Custom Annotations*: Add morphology information or custom notes directly beneath words for reference during reading
- *Chunk Annotations*: Mark and annotate larger grammatical structures (phrases, clauses)

**In Development**
- *Automatic Syntax Labeling*: Identify and highlight common syntactic patterns (ablative absolutes, conditionals, dative of possession, etc.) using Perseus treebank queries
- *Learner Analytics*: Track error patterns to generate personalized study recommendations

### Technologies
Frontend: Vue.js  
Data Source: Perseus Project treebanks  
Preprocessing: XML treebank files are preprocessed using the tb_to_json.py script in data_gen/. Automatic Syntax Labeling is performed with a modified version of [pseudw python](https://github.com/zspriggs/pseudw_python), a Python version of nkallen's [pseudw](https://github.com/nkallen/pseudw). 

### About
Juno is being developed as a master's thesis project by Zoe Spriggs and Mitchell Shiffer. User testing with students is planned for Spring 2026 to evaluate effectiveness and refine features based on learner feedback. If you have feedback on Juno or feature suggestions, we'd love to hear it! Please reach out to [zoe.spriggs@tufts.edu](mailto:zoe.spriggs@tufts.edu) or open a GitHub Issue. 

**Development Notes**
This project has been developed with assistance from AI coding tools (Gemini, Claude, etc.). Code structure and implementation decisions are my own, with AI serving as a pair programming assistant.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgments
We are grateful to the developers and annotators of [The Ancient Greek and Latin Dependency Treebank](https://perseusdl.github.io/treebank_data/) 

