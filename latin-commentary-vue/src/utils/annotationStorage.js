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
    }
};