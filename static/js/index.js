// Track edit modes
let isLayoutMode = false;
let activeTable = null;

// Initialize seats for all tables
document.addEventListener('DOMContentLoaded', function() {
    const cells = document.querySelectorAll('.cell');
    cells.forEach(cell => {
        renderSeats(cell);
    });
    
    // Show layout mode option
    document.getElementById('edit-mode-toggle').addEventListener('change', function() {
        isLayoutMode = this.checked;
        document.body.classList.toggle('layout-mode', isLayoutMode);
    });
    
    // Close modal when clicking the close button
    document.getElementById('close-modal').addEventListener('click', function() {
        closeTableModal();
    });
    
    // Close modal when clicking outside
    document.getElementById('table-edit-modal').addEventListener('click', function(e) {
        if (e.target === this) {
            closeTableModal();
        }
    });
    
    // Save changes button
    document.getElementById('save-table-changes').addEventListener('click', function() {
        saveTableChanges();
    });
    
    // Add event listeners for seat control buttons in modal
    document.getElementById('decrease-seats-btn').addEventListener('click', function() {
        const seatCountElement = document.getElementById('seat-count-display');
        let currentSeats = parseInt(seatCountElement.textContent);
        if (currentSeats > 1) {
            seatCountElement.textContent = --currentSeats;
        }
    });
    
    document.getElementById('increase-seats-btn').addEventListener('click', function() {
        const seatCountElement = document.getElementById('seat-count-display');
        let currentSeats = parseInt(seatCountElement.textContent);
        if (currentSeats < 8) {
            seatCountElement.textContent = ++currentSeats;
        }
    });
    
    // View mode toggles
    document.querySelector('.employee-pov').addEventListener('click', function() {
        this.classList.add('active');
        document.querySelector('.manager-pov').classList.remove('active');
    });

    document.querySelector('.manager-pov').addEventListener('click', function() {
        this.classList.add('active');
        document.querySelector('.employee-pov').classList.remove('active');
    });
    
    // Initialize layout from saved data
    loadLayout();
});

// Handle cell click based on current mode
function handleCellClick(element) {
    if (isLayoutMode) {
        // In layout mode, show the edit modal
        if (!element.classList.contains('floor')) {
            showTableEditModal(element);
        } else {
            // Toggle between table and floor
            toggleCellType(element);
        }
    } else {
        // In normal mode, toggle table status (only if it's a table)
        if (!element.classList.contains('floor')) {
            toggleTableStatus(element);
        }
    }
}

// Show the table edit modal
function showTableEditModal(element) {
    activeTable = element;
    
    const modal = document.getElementById('table-edit-modal');
    const tableName = document.getElementById('table-name-input');
    const seatCount = document.getElementById('seat-count-display');
    const occupiedCheckbox = document.getElementById('table-occupied');
    const toggleFloorBtn = document.getElementById('toggle-floor-btn');
    
    // Fill in current values
    tableName.value = element.dataset.customName || element.querySelector('.cell-label').textContent;
    seatCount.textContent = element.dataset.seats;
    occupiedCheckbox.checked = element.classList.contains('occupied');
    
    // Show the modal
    modal.style.display = 'flex';
    tableName.focus();
    tableName.select();
}

// Close the table edit modal
function closeTableModal() {
    document.getElementById('table-edit-modal').style.display = 'none';
    activeTable = null;
}

// Save changes from the modal
function saveTableChanges() {
    if (!activeTable) return;
    
    // Get values from modal
    const newName = document.getElementById('table-name-input').value.trim();
    const newSeatCount = parseInt(document.getElementById('seat-count-display').textContent);
    const isOccupied = document.getElementById('table-occupied').checked;
    const makeFloor = document.getElementById('make-floor').checked;
    
    if (makeFloor) {
        // Convert to floor space
        activeTable.classList.add('floor');
        activeTable.classList.remove('occupied');
        
        // Update display for floor space
        const statusIndicator = activeTable.querySelector('.status-indicator');
        statusIndicator.style.display = 'none';
        
        const cellLabel = activeTable.querySelector('.cell-label');
        cellLabel.textContent = 'Floor Space';
        
        // Hide seats container
        const seatsContainer = activeTable.querySelector('.seats-container');
        seatsContainer.style.display = 'none';
    } else {
        // Ensure it's a table, not floor
        activeTable.classList.remove('floor');
        
        // Update table name
        if (newName) {
            activeTable.dataset.customName = newName;
            activeTable.querySelector('.cell-label').textContent = newName;
        } else {
            // If empty, revert to default name
            const row = parseInt(activeTable.dataset.row);
            const col = parseInt(activeTable.dataset.col);
            const tableNum = row * 5 + col + 1;
            
            delete activeTable.dataset.customName;
            activeTable.querySelector('.cell-label').textContent = 'Table #' + tableNum;
        }
        
        // Update seat count
        activeTable.dataset.seats = newSeatCount;
        
        // Update occupied status
        if (isOccupied) {
            activeTable.classList.add('occupied');
            activeTable.querySelector('.status-indicator').classList.add('occupied');
        } else {
            activeTable.classList.remove('occupied');
            activeTable.querySelector('.status-indicator').classList.remove('occupied');
        }
        
        // Show status indicator
        const statusIndicator = activeTable.querySelector('.status-indicator');
        statusIndicator.style.display = 'block';
        
        // Show seats container
        const seatsContainer = activeTable.querySelector('.seats-container');
        seatsContainer.style.display = 'flex';
        
        // Render seats
        renderSeats(activeTable);
    }
    
    // Close modal and save layout
    closeTableModal();
    saveLayout();
}

// Render seat indicators based on the number of seats
function renderSeats(cell) {
    if (cell.classList.contains('floor')) return;
    
    const seatsContainer = cell.querySelector('.seats-container');
    const seatCount = parseInt(cell.dataset.seats);
    
    // Clear existing seats
    seatsContainer.innerHTML = '';
    
    // Add new seat indicators
    for (let i = 0; i < seatCount; i++) {
        const seat = document.createElement('div');
        seat.className = 'seat';
        if (cell.classList.contains('occupied')) {
            seat.classList.add('occupied');
        }
        seatsContainer.appendChild(seat);
    }
}

// Toggle between table and floor space
function toggleCellType(element) {
    element.classList.toggle('floor');
    
    if (element.classList.contains('floor')) {
        // If changing to floor, remove occupied status if present
        element.classList.remove('occupied');
        
        // Update display for floor space
        const statusIndicator = element.querySelector('.status-indicator');
        statusIndicator.style.display = 'none';
        
        const cellLabel = element.querySelector('.cell-label');
        cellLabel.textContent = 'Floor Space';
        
        // Hide seats container
        const seatsContainer = element.querySelector('.seats-container');
        seatsContainer.style.display = 'none';
    } else {
        // Restore table display
        const statusIndicator = element.querySelector('.status-indicator');
        statusIndicator.style.display = 'block';
        
        const row = element.dataset.row;
        const col = element.dataset.col;
        const tableNum = parseInt(row) * 5 + parseInt(col) + 1;
        
        const cellLabel = element.querySelector('.cell-label');
        
        // Use custom name if it exists, otherwise use default table number
        if (element.dataset.customName) {
            cellLabel.textContent = element.dataset.customName;
        } else {
            cellLabel.textContent = 'Table #' + tableNum;
        }
        
        // Show seats container
        const seatsContainer = element.querySelector('.seats-container');
        seatsContainer.style.display = 'flex';
        
        // Render seats
        renderSeats(element);
    }
    
    saveLayout();
}

// Toggle table occupied status
function toggleTableStatus(element) {
    element.classList.toggle('occupied');
    const statusIndicator = element.querySelector('.status-indicator');
    statusIndicator.classList.toggle('occupied');
    
    // Update seat indicators to match table status
    const seats = element.querySelectorAll('.seat');
    seats.forEach(seat => {
        seat.classList.toggle('occupied');
    });
    
    saveLayout();
}

// Save layout to localStorage
function saveLayout() {
    const cells = document.querySelectorAll('.cell');
    const layoutData = [];
    
    cells.forEach(cell => {
        layoutData.push({
            id: cell.id,
            isFloor: cell.classList.contains('floor'),
            isOccupied: cell.classList.contains('occupied'),
            seats: parseInt(cell.dataset.seats),
            customName: cell.dataset.customName || null
        });
    });
    
    localStorage.setItem('restaurantLayout', JSON.stringify(layoutData));
}

// Load layout from localStorage
function loadLayout() {
    const savedLayout = localStorage.getItem('restaurantLayout');
    if (!savedLayout) return;
    
    const layoutData = JSON.parse(savedLayout);
    
    layoutData.forEach(item => {
        const cell = document.getElementById(item.id);
        if (!cell) return;
        
        // Reset cell
        cell.classList.remove('floor', 'occupied');
        
        // Apply saved properties
        if (item.isFloor) {
            cell.classList.add('floor');
            cell.querySelector('.status-indicator').style.display = 'none';
            cell.querySelector('.cell-label').textContent = 'Floor Space';
            cell.querySelector('.seats-container').style.display = 'none';
        } else {
            cell.querySelector('.status-indicator').style.display = 'block';
            cell.querySelector('.seats-container').style.display = 'flex';
            
            // Set custom name if it exists
            if (item.customName) {
                cell.dataset.customName = item.customName;
                cell.querySelector('.cell-label').textContent = item.customName;
            } else {
                const row = parseInt(cell.dataset.row);
                const col = parseInt(cell.dataset.col);
                const tableNum = row * 5 + col + 1;
                cell.querySelector('.cell-label').textContent = 'Table #' + tableNum;
            }
            
            if (item.isOccupied) {
                cell.classList.add('occupied');
                cell.querySelector('.status-indicator').classList.add('occupied');
            } else {
                cell.querySelector('.status-indicator').classList.remove('occupied');
            }
        }
        
        // Update seats
        cell.dataset.seats = item.seats || 4;
        renderSeats(cell);
    });
}