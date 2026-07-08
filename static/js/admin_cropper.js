document.addEventListener('DOMContentLoaded', function() {
    // 1. Inject Modal HTML into the body
    const modalHtml = `
    <div id="admin-cropper-modal" style="display:none; position:fixed; z-index:99999; left:0; top:0; width:100%; height:100%; background:rgba(0,0,0,0.8); align-items:center; justify-content:center; flex-direction:column;">
        <div style="background:#fff; padding:20px; border-radius:8px; max-width:90%; max-height:90%; display:flex; flex-direction:column; gap:15px; box-shadow:0 10px 25px rgba(0,0,0,0.5);">
            <h3 style="margin:0; font-family:sans-serif; font-size:18px; color:#333;">Обрезка изображения</h3>
            <div style="width:100%; height:60vh; max-height:600px; background:#f0f0f0; display:flex; justify-content:center; align-items:center; overflow:hidden;">
                <img id="admin-cropper-image" style="max-width:100%; max-height:100%; display:block;" src="" alt="Picture">
            </div>
            <div style="display:flex; justify-content:flex-end; gap:10px;">
                <button type="button" id="admin-cropper-cancel" style="padding:8px 16px; border:none; background:#ccc; color:#333; border-radius:4px; cursor:pointer; font-weight:bold;">Отмена</button>
                <button type="button" id="admin-cropper-apply" style="padding:8px 16px; border:none; background:#e11d48; color:#fff; border-radius:4px; cursor:pointer; font-weight:bold;">Применить кроп</button>
            </div>
        </div>
    </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHtml);

    const modal = document.getElementById('admin-cropper-modal');
    const imageElement = document.getElementById('admin-cropper-image');
    const btnCancel = document.getElementById('admin-cropper-cancel');
    const btnApply = document.getElementById('admin-cropper-apply');

    let cropper = null;
    let currentInput = null;
    let currentFile = null;

    function closeModal() {
        modal.style.display = 'none';
        if (cropper) {
            cropper.destroy();
            cropper = null;
        }
        currentInput = null;
        currentFile = null;
    }

    btnCancel.addEventListener('click', function() {
        // If canceled, we clear the input so they can try again
        if (currentInput) {
            currentInput.value = '';
            // If unfold has a custom label, trigger change to reset it
            currentInput.dataset.cropped = '';
            currentInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
        closeModal();
    });

    btnApply.addEventListener('click', function() {
        if (!cropper || !currentInput) return;

        cropper.getCroppedCanvas({
            imageSmoothingEnabled: true,
            imageSmoothingQuality: 'high',
        }).toBlob(function(blob) {
            if (!blob) {
                alert('Ошибка при обрезке');
                return;
            }

            // Create a new File from the blob
            const newFile = new File([blob], 'cropped_' + currentFile.name, { type: blob.type || 'image/jpeg' });
            
            // Replace the files array
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(newFile);
            currentInput.files = dataTransfer.files;
            
            // Mark as cropped to prevent infinite loop
            currentInput.dataset.cropped = 'true';
            
            // Trigger change event for Unfold UI
            currentInput.dispatchEvent(new Event('change', { bubbles: true }));
            
            closeModal();
        }, currentFile.type === 'image/png' ? 'image/png' : 'image/jpeg', 0.9);
    });

    // Find all file inputs that belong to image fields (including translated ones)
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        if (!input.id) return;
        
        // Determine aspect ratio based on input ID
        let aspectRatio = null;
        if (input.id.startsWith('id_image_mobile')) {
            aspectRatio = 9 / 16;
        } else if (input.id.startsWith('id_image')) {
            aspectRatio = 21 / 9;
        }
        
        if (!aspectRatio) return;

        input.addEventListener('change', function(e) {
            // Avoid triggering if we just programmatically replaced the file
            if (this.dataset.cropped === 'true') {
                this.dataset.cropped = ''; // reset for future manual changes
                return;
            }

            if (this.files && this.files.length > 0) {
                const file = this.files[0];
                if (!file.type.startsWith('image/')) return;

                currentInput = this;
                currentFile = file;

                const reader = new FileReader();
                reader.onload = function(evt) {
                    modal.style.display = 'flex';
                    
                    imageElement.onload = function() {
                        // Small delay to ensure CSS layout is fully calculated
                        setTimeout(function() {
                            if (cropper) cropper.destroy();
                            cropper = new Cropper(imageElement, {
                                aspectRatio: aspectRatio,
                                viewMode: 1, // Restrict crop box to not exceed canvas
                                autoCropArea: 1,
                                background: false,
                                zoomable: true,
                                guides: true,
                            });
                        }, 50);
                        imageElement.onload = null;
                    };
                    
                    imageElement.src = evt.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });
});
