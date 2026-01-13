<template>
  <div class="help-display">
    <h3 class="title">Using Juno</h3>
    <h4 class="subtitle">ADDING ANNOTATIONS</h4>
    <pre class="help-text">Click a word to open up the <strong>Annotation Menu</strong> on the right side of the screen.

        Select morphology (i.e. case, tense, gender) in the Annotation Menu.

        Click <strong>Check</strong> on the annotation menu to check your labels. 

        After checking, click <strong>Add</strong> to add the labels onto the text, under the word.

        Custom inline annotations may be added via the annotation menu at any time.

        Click and drag over a group of words to create a <strong>chunk annotation.</strong> After creating a chunk annotation, the annotation can be accessed or deleted by clicking the 💬 icon.
    </pre>
    <h4 class="subtitle"> SAVING ANNOTATIONS</h4>
    <pre class="help-text">
    To save annotations, open the <strong>⚙️ Settings</strong> menu on the upper right hand side of the screen and click <strong>Export Annotations.</strong>

    This will save a JSON file, which can later be uploaded with <strong>Import Annotations</strong> on any device. Imported annotations will merge with existing annotations.
    </pre>
    
    <h3 class="title">About</h3>
    <pre class="help-text">
        Juno is being created by Zoë Spriggs and Mitchell Shiffer, as part of a joint master's thesis project.

        For more information on the project, please visit https://github.com/zspriggs/juno-reader
        
        Special thanks
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
