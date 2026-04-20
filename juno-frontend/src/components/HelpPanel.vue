<template>
  <div class="help-display">
    <h3 class="title">Using Juno: Quick Start</h3>
    <h4 class="subtitle">ADDING ANNOTATIONS</h4>
    <pre class="help-text">Click a word to open up the <strong>Annotation Menu</strong>.

        Select attributes (i.e. case, number, gender) in the Annotation Menu, then click <strong>Check</strong> to check your work.

        After checking, click <strong>Add</strong> to add the annotations you got correct onto the text. You can also <strong>Add</strong> custom (unchecked) annotations.

        Click and drag over a group of words to create a <strong>chunk annotation.</strong> After creating a chunk annotation, the annotation can be viewed or deleted by clicking the 💬 icon.
    </pre>
    <h4 class="subtitle"> SAVING ANNOTATIONS</h4>
    <pre class="help-text">
    To save annotations, open the <strong>⚙️ Settings</strong> menu on the upper right hand side of the screen and click <strong>Export Annotations.</strong>

    This will save a JSON file, which can later be uploaded with <strong>Import Annotations</strong> on any device. Imported annotations will merge with existing annotations.
    </pre>

    <h3 class="title">About</h3>
    <pre class="help-text">
    Juno is being created by Zoë Spriggs and Mitchell Shiffer, as part of a master's thesis project.

    For more information on the project, including the code, visit our <a href="https://github.com/zspriggs/juno-reader">GitHub page.</a>

    Please send any questions, issues, or suggestions to zoe.spriggs2@gmail.com
    </pre>

    <h3 class="title">Data Credit</h3>
    <pre class="help-text">
    This project uses data from the <a href="https://perseusdl.github.io/treebank_data/" target="_blank">Ancient Greek and Latin Dependency Treebank</a> (AGLDT) and <a href="https://github.com/alekkeersmaekers/glaux" target="_blank">Greek Language Automated </a>(GLAUx) treebank.

    Bamman, David, and Gregory Crane (2011) “The Ancient Greek and Latin Dependency Treebanks.” https://people.ischool.berkeley.edu/~dbamman/pubs/pdf/latech2011.pdf.

    Keersmaekers, Alek (2021): The GLAUx corpus: methodological issues in designing a long-term, diverse, multi-layered corpus of Ancient Greek. Proceedings of the 2nd International Workshop on Computational Approaches to Historical Language Change 2021, 39–50. Online: Association for Computational Linguistics. doi:10.18653/v1/2021.lchange-1.6.
    </pre>
  </div>
</template>

<script setup>
</script>

<style scoped>
.help-text {
    font-family: inherit;
    white-space: pre-line;
    font-size: 1rem;
}

.title {
    color: var(--title-dark);
}

.subtitle {
    color: var(--gray-text);
}
</style>
