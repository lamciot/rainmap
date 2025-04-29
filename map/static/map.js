// Grid dimensions
const COLS = 50;
const ROWS = 30;

// Create empty grid data structure
let gridData = Array(ROWS).fill().map(() => Array(COLS).fill(0));

// Get color based on value
function getColorForValue(value) {
    value = parseFloat(value);
    
    if (value <= 0) return 'transparent';
    
    // Blue to Aqua to Yellow gradient
    if (value <= 0.5) {
        // Blue (0.1-0.5)
        const intensity = (value - 0.1) / 0.4; // Normalize to 0-1
        const alpha = Math.min(0.7, 0.3 + intensity * 0.4);
        return `rgba(0, 0, ${Math.floor(128 + intensity * 127)}, ${alpha})`;
    }
    else if (value <= 1.0) {
        // Aqua (0.5-1.0)
        const intensity = (value - 0.5) / 0.5; // Normalize to 0-1
        const alpha = 0.7;
        return `rgba(0, ${Math.floor(128 + intensity * 127)}, ${Math.floor(255 - intensity * 127)}, ${alpha})`;
    }
    else {
        // Yellow (1.0-3.0)
        const intensity = Math.min(1, (value - 1.0) / 2.0); // Normalize to 0-1
        const alpha = 0.5 + intensity * 0.3;
        return `rgba(255, 255, ${Math.floor(200 - intensity * 150)}, ${alpha})`;
    }
}

// Initialize the grid with transparent cells
function initGrid() {
    const grid = document.getElementById('grid');
    grid.innerHTML = '';
    
    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLS; col++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.row = row;
            cell.dataset.col = col;
            cell.dataset.value = 0;
            
            // Click to increase value
            // cell.addEventListener('click', function() {
            //     const currentVal = parseFloat(this.dataset.value) || 0;
            //     let newVal = currentVal + 0.1;
            //     if (newVal > 3.0) newVal = 0;
            //     this.dataset.value = newVal.toFixed(1);
            //     this.style.backgroundColor = getColorForValue(newVal);
            // });
            
            grid.appendChild(cell);
        }
    }
}

// Update grid with data
function updateGrid(data) {
    const cells = document.querySelectorAll('.cell');
    
    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLS; col++) {
            const value = data[row][col];
            const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
            
            if (cell) {
                cell.dataset.value = value;
                cell.style.backgroundColor = getColorForValue(value);
            }
        }
    }
}

// Parse input data
function parseInputData(input) {
    const lines = input.trim().split('\n');
    const data = [];
    
    for (let row = 0; row < ROWS; row++) {
        const line = lines[row] || '';
        // Split by commas or whitespace
        const values = line.split(/[, \t]+/).filter(v => v !== '');
        const rowData = [];
        
        for (let col = 0; col < COLS; col++) {
            // Use 0 if no data provided
            const value = parseFloat(values[col]) || 0;
            // Clamp to 0-3 range
            rowData[col] = Math.max(0, Math.min(3.0, value));
        }
        
        data.push(rowData);
    }
    
    return data;
}
// disable minute form
document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.querySelector('input[type="datetime-local"]');
    dateInput.addEventListener('input', function() {
        if (!this.value) return;
        
        const date = new Date(this.value);
        if (date.getMinutes() !== 0) {
            date.setMinutes(0);
            this.value = date.toISOString().slice(0, 16);
        }
    });
    
    // Optional: Force initial value to whole hour
    // if (dateInput.value) {
    //     const date = new Date(dateInput.value);
    //     if (date.getMinutes() !== 0) {
    //     date.setMinutes(0);
    //     dateInput.value = date.toISOString().slice(0, 16);
    //     }
    // }
});
// alredy display message
function clickMess() {
    document.getElementById("noti").innerHTML = "Đã hiển thị dữ liệu";
}

// Event listeners
// document.getElementById('applyData').addEventListener('click', function() {
//     // const input = document.getElementById('dataInput');
//     const dataInput = document.getElementById('dataInput').dataset.value;
//     try {
//         const data = JSON.parse(document.getElementById('dataInput').textContent);
//         console.log('Parsed data:', data);
//     } catch (e) {
//         console.error('Parsing error:', e);
//     }
//     // const inputData = JSON.parse(dataInput.dataset.input);
//     console.log("THe data is ",dataInput);
//     const parsedData = parseInputData(dataInput);
//     updateGrid(parsedData);
// });

document.getElementById('applyData').addEventListener('click', function() {
    const input = document.getElementById('dataInput').value;
    const parsedData = parseInputData(input);
    updateGrid(parsedData);
});

// document.getElementById('clearGrid').addEventListener('click', function() {
//     document.getElementById('dataInput').value = '';
//     const emptyData = Array(ROWS).fill().map(() => Array(COLS).fill(0));
//     updateGrid(emptyData);
// });

// const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Initialize the grid on page load
window.onload = initGrid;
