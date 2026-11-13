/**
 * Interactive Visual Seating Grid Handler for ParikshaVinyas
 */
document.addEventListener('DOMContentLoaded', function() {
    const seatModalEl = document.getElementById('seatDetailModal');
    let seatModal = null;
    if (seatModalEl && window.bootstrap) {
        seatModal = new bootstrap.Modal(seatModalEl);
    }

    // Handle seat click in visual allocation grid
    document.querySelectorAll('.seat-clickable').forEach(function(seat) {
        seat.addEventListener('click', function() {
            const status = seat.getAttribute('data-status');
            const ident = seat.getAttribute('data-ident');
            const row = seat.getAttribute('data-row');
            const col = seat.getAttribute('data-col');
            const name = seat.getAttribute('data-student-name') || 'None';
            const enroll = seat.getAttribute('data-student-enroll') || 'None';
            const course = seat.getAttribute('data-student-course') || '-';
            const div = seat.getAttribute('data-student-div') || '-';
            const strategy = seat.getAttribute('data-strategy') || 'N/A';
            const reason = seat.getAttribute('data-reason') || '';

            const modalTitle = document.getElementById('seatModalTitle');
            const modalBody = document.getElementById('seatModalBody');

            if (modalTitle) modalTitle.textContent = `Seat Details: ${ident}`;

            let html = `
                <div class="list-group list-group-flush">
                    <div class="list-group-item d-flex justify-content-between">
                        <strong>Position:</strong> <span>Row ${row}, Column ${col}</span>
                    </div>
                    <div class="list-group-item d-flex justify-content-between">
                        <strong>Status:</strong> 
                        <span class="badge ${status === 'allocated' ? 'bg-primary' : (status === 'blocked' ? 'bg-danger' : 'bg-success')} text-uppercase">${status}</span>
                    </div>`;

            if (status === 'allocated') {
                html += `
                    <div class="list-group-item d-flex justify-content-between">
                        <strong>Candidate Name:</strong> <span class="fw-bold">${name}</span>
                    </div>
                    <div class="list-group-item d-flex justify-content-between">
                        <strong>Enrollment No:</strong> <code>${enroll}</code>
                    </div>
                    <div class="list-group-item d-flex justify-content-between">
                        <strong>Course & Division:</strong> <span>${course} (Div ${div})</span>
                    </div>
                    <div class="list-group-item d-flex justify-content-between">
                        <strong>Allocation Strategy:</strong> <span class="text-muted">${strategy}</span>
                    </div>`;
            } else if (status === 'blocked') {
                html += `
                    <div class="list-group-item d-flex justify-content-between">
                        <strong>Blocking Reason:</strong> <span class="text-danger">${reason || 'Seat marked as damaged or reserved.'}</span>
                    </div>`;
            } else {
                html += `
                    <div class="list-group-item text-muted">
                        This seat is physically available and unassigned.
                    </div>`;
            }
            html += `</div>`;

            if (modalBody) modalBody.innerHTML = html;
            if (seatModal) seatModal.show();
        });
    });

    // Handle seat toggle click in Hall Layout editor
    document.querySelectorAll('.seat-toggle-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const hallId = btn.getAttribute('data-hall-id');
            const row = btn.getAttribute('data-row');
            const col = btn.getAttribute('data-col');
            const ident = btn.getAttribute('data-ident');

            if (!confirm(`Toggle blocked/available state for seat ${ident}?`)) {
                return;
            }

            fetch(`/admin/halls/${hallId}/toggle-seat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': (document.querySelector('meta[name="csrf-token"]') || {}).content || ''
                },
                body: JSON.stringify({ row: parseInt(row), col: parseInt(col) })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert(data.message || 'Error toggling seat state.');
                }
            })
            .catch(err => {
                console.error(err);
                location.reload();
            });
        });
    });
});

