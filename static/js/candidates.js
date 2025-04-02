document.addEventListener('DOMContentLoaded', function() {
    console.log('Script loaded'); // Debug print
    
    // Get all candidate cards
    const cards = document.querySelectorAll('.card-content');
    console.log('Found cards:', cards.length); // Debug print
    
    const modal = document.getElementById('pdfModal');
    const modalTitle = document.getElementById('pdfModalTitle');
    const pdfFrame = document.getElementById('pdfFrame');
    const closeBtn = document.querySelector('.pdf-close');

    // Debug print all elements
    console.log('Elements found:', {
        modal: modal !== null,
        modalTitle: modalTitle !== null,
        pdfFrame: pdfFrame !== null,
        closeBtn: closeBtn !== null
    });

    // Debug print card data
    cards.forEach(card => {
        console.log('Card data attributes:', {
            pdfUrl: card.dataset.pdfUrl,
            name: card.dataset.name
        });
        
        // Add click event to cards
        card.addEventListener('click', function(e) {
            console.log('Card clicked'); // Debug print
            console.log('Card data:', {  // Debug print
                pdfUrl: this.dataset.pdfUrl,
                name: this.dataset.name
            });
            
            e.preventDefault();
            e.stopPropagation();
            
            const pdfUrl = this.dataset.pdfUrl;
            const name = this.dataset.name;
            
            if (!pdfUrl) {
                console.error('No PDF URL found for this candidate');
                return;
            }
            
            // Set modal content
            modalTitle.textContent = name;
            pdfFrame.src = pdfUrl;
            
            // Show modal
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        });
    });

    // Close modal when clicking X
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            closeModal();
        });
    }

    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    // Close modal function
    function closeModal() {
        modal.style.display = 'none';
        pdfFrame.src = '';
        document.body.style.overflow = 'auto';
    }

    // Close modal with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal.style.display === 'block') {
            closeModal();
        }
    });
}); 