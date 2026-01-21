export const storageUtil = {    
    save(key, annotations) {
        try {
            localStorage.setItem(key, JSON.stringify(annotations));
            return true;
        }
        catch (e) {
            console.error("Failed to save.");
            return false;
        }
    },

    load(key) {
        try {
            const saved = localStorage.getItem(key);
            return saved ? JSON.parse(saved) : {};
        } 
        catch (e) {
            console.error("Failed to load: ", e);
            return {};
        }
    },

    clear(key) {
        localStorage.removeItem(key);
    },

    export(key) {
        const data = localStorage.getItem(key) || '{}';
        const blob = new Blob([data], {type: `${key}/json`});
        const tempurl = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = tempurl;
        link.download = `${key}-${new Date().toLocaleString()}.json`
        link.click();
        URL.revokeObjectURL(tempurl);
    },

    import(key, callback) {
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
                    this.save(key, importedData);
                    
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