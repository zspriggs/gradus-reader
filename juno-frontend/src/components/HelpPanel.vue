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

    <h3 class="title">Data Credit</h3>
    <pre class="help-text">
        This project uses data from the Ancient Greek and Latin Dependency Treebanks (AGLDT) and Greek Language Automated (GLAUx) corpora.
    </pre>
    
    <h3 class="title">About</h3>
    <pre class="help-text">
        Juno is being created by Zoë Spriggs and Mitchell Shiffer, as part of a master's thesis project.

        For more information on the project, including the code, visit our <a href="https://github.com/zspriggs/juno-reader">GitHub page.</a>

        Feel free to send any questions, issues, or suggestions to zoe.spriggs@tufts.edu
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
