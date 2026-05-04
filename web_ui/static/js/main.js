// main.js
document.addEventListener('DOMContentLoaded', () => {
    const opItems = document.querySelectorAll('.op-item');
    const recipeContainer = document.getElementById('recipe-container');
    const bakeBtn = document.getElementById('bake-btn');
    const inputText = document.getElementById('input-text');
    const outputText = document.getElementById('output-text');
    const clearRecipeBtn = document.getElementById('clear-recipe');
    const opSearch = document.getElementById('op-search');

    let recipe = [];

    // Search functionality
    opSearch.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        opItems.forEach(item => {
            const opName = item.dataset.op.toLowerCase();
            if (opName.includes(query)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    });

    // Drag and Drop Logic
    opItems.forEach(item => {
        item.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text', JSON.stringify({
                name: item.dataset.op,
                args: item.dataset.args ? item.dataset.args.split(',') : []
            }));
            e.dataTransfer.effectAllowed = 'copy';
        });
    });

    recipeContainer.addEventListener('dragenter', (e) => {
        e.preventDefault();
        recipeContainer.classList.add('drag-over');
    });

    recipeContainer.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
        recipeContainer.classList.add('drag-over');
    });

    recipeContainer.addEventListener('dragleave', (e) => {
        recipeContainer.classList.remove('drag-over');
    });

    recipeContainer.addEventListener('drop', (e) => {
        e.preventDefault();
        recipeContainer.classList.remove('drag-over');
        
        try {
            const data = JSON.parse(e.dataTransfer.getData('text'));
            if(data && data.name) {
                addOperationToRecipe(data);
            }
        } catch (err) {
            console.error("Drop error", err);
        }
    });

    // Support double click to add
    opItems.forEach(item => {
        item.addEventListener('dblclick', () => {
            addOperationToRecipe({
                name: item.dataset.op,
                args: item.dataset.args ? item.dataset.args.split(',') : []
            });
        });
    });

    function addOperationToRecipe(opData) {
        // Remove placeholder if present
        const placeholder = recipeContainer.querySelector('.recipe-placeholder');
        if (placeholder) placeholder.remove();

        const opId = Date.now().toString() + Math.random().toString(36).substr(2, 5);
        const opEntry = {
            id: opId,
            name: opData.name,
            argsData: {}
        };

        recipe.push(opEntry);

        const opEl = document.createElement('div');
        opEl.className = 'recipe-item';
        opEl.dataset.id = opId;

        let argsHtml = '';
        if (opData.args && opData.args.length > 0) {
            argsHtml = '<div class="recipe-args">';
            opData.args.forEach(arg => {
                if (arg.trim() === '') return;
                argsHtml += `
                    <label>${arg.charAt(0).toUpperCase() + arg.slice(1)}</label>
                    <input type="text" class="op-arg" data-arg="${arg}" placeholder="Enter ${arg}">
                `;
            });
            argsHtml += '</div>';
        }

        opEl.innerHTML = `
            <div class="recipe-item-header">
                <span>${opData.name}</span>
                <button class="remove-op" title="Remove">&times;</button>
            </div>
            ${argsHtml}
        `;

        // Handle arg inputs
        const inputs = opEl.querySelectorAll('.op-arg');
        inputs.forEach(input => {
            input.addEventListener('input', (e) => {
                const argName = e.target.dataset.arg;
                const r = recipe.find(item => item.id === opId);
                if (r) r.argsData[argName] = e.target.value;
                autoBake();
            });
        });

        // Handle remove
        const removeBtn = opEl.querySelector('.remove-op');
        removeBtn.addEventListener('click', () => {
            opEl.remove();
            recipe = recipe.filter(item => item.id !== opId);
            if (recipe.length === 0) {
                recipeContainer.innerHTML = '<div class="recipe-placeholder">Drag operations here or Double Click</div>';
            }
            autoBake();
        });

        recipeContainer.appendChild(opEl);
        autoBake();
    }

    clearRecipeBtn.addEventListener('click', () => {
        recipe = [];
        recipeContainer.innerHTML = '<div class="recipe-placeholder">Drag operations here or Double Click</div>';
        autoBake();
    });

    inputText.addEventListener('input', () => {
        autoBake();
    });

    bakeBtn.addEventListener('click', () => {
        bake();
    });

    // Auto-bake debounce
    let timeoutId;
    function autoBake() {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            bake();
        }, 300);
    }

    async function bake() {
        const inputVal = inputText.value;
        if (!inputVal) {
            outputText.value = '';
            return;
        }

        if (recipe.length === 0) {
            outputText.value = inputVal;
            return;
        }

        const formattedOps = recipe.map(r => {
            const op = { name: r.name };
            if (r.argsData) {
                Object.assign(op, r.argsData);
            }
            return op;
        });

        outputText.value = 'Baking...';

        try {
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    input: inputVal,
                    operations: formattedOps
                })
            });

            const data = await response.json();
            
            if (data.success) {
                outputText.value = data.output;
            } else {
                outputText.value = 'Error: ' + data.error;
            }
        } catch (error) {
            outputText.value = 'Network Error: ' + error.message;
        }
    }
});
