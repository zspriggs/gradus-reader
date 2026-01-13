export const annotationStorage = {
    STORAGE_KEY: 'annotationz',
    
    save(annotations) {
        try {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(annotations));
            return true;
        }
        catch (e) {
            console.error("Failed to save annotations.");
            return false;
        }
    },

    load() {
        try {
            const saved = localStorage.getItem(this.STORAGE_KEY);
            return saved ? JSON.parse(saved) : {};
        } 
        catch (e) {
            console.error("Failed to load annotations: ", e);
            return {};
        }
    },

    clear() {
        localStorage.removeItem(this.STORAGE_KEY);
    },

    export() {
        const data = localStorage.getItem(this.STORAGE_KEY) || '{}';
        const blob = new Blob([data], {type: 'annotations/json'});
        const tempurl = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = tempurl;
        link.download = `annotations-${new Date().toLocaleString()}.json`
        link.click();
        URL.revokeObjectURL(tempurl);
    },

    import(callback) {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';

        input.onchange = (event) => {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const importedData = JSON.parse(e.target.result);
                    
                    // Save the data to localStorage
                    this.save(importedData);
                    
                    // Trigger a callback so the UI can refresh
                    if (callback) callback(importedData);
                    
                    console.log("Import successful!");
                } catch (err) {
                    console.error("Failed to parse import file:", err);
                    alert("Invalid file format. Please upload a valid JSON file.");
                }
            };
            reader.readAsText(file);
        };
        input.click();
    }
};