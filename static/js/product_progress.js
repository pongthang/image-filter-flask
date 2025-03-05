document.addEventListener("DOMContentLoaded", async () => {
    // Helper function to check product completion status
    const isProductComplete = (files) => {
        return files.every(file =>
            !['PENDING', 'RERUN'].includes(file.first_pass_status) &&
            !['PENDING', 'RERUN'].includes(file.face_swap_status) &&
            !['PENDING', 'RERUN'].includes(file.hand_fix_status) &&
            !['PENDING', 'RERUN'].includes(file.upscale_status)
        );
    };

    // Generate file row HTML
    const createFileRows = (images, productId) => {
        if (!images.length) {
            return `
                <tr>
                    <td colspan="5">No files available</td>
                </tr>`;
        }

        return images.map(file => `
            <tr>
                <td>${file.image_path}</td>
                <td class="${file.first_pass_status === 'PENDING' ? 'status-pending' : ''}" 
                    data-status="${file.first_pass_status}">${file.first_pass_status}</td>
                <td class="${file.face_swap_status === 'PENDING' ? 'status-pending' : ''}" 
                    data-status="${file.face_swap_status}">${file.face_swap_status}</td>
                <td class="${file.hand_fix_status === 'PENDING' ? 'status-pending' : ''}" 
                    data-status="${file.hand_fix_status}">${file.hand_fix_status}</td>
                <td class="${file.upscale_status === 'PENDING' ? 'status-pending' : ''}" 
                    data-status="${file.upscale_status}">${file.upscale_status}</td>
            </tr>
        `).join('');
    };

    try {
        // Fetch products
        const response = await fetch("/api/products");
        const products = await response.json();
        const tableBody = document.querySelector("#productTableBody");

        // Build table rows
        products.forEach(product => {
            const productStatus = isProductComplete(product.images) ? "COMPLETE" : "NOT COMPLETE";

            // Product row
            const productRow = document.createElement("tr");
            productRow.classList.add("product-row");
            productRow.innerHTML = `
                <td class="expandable" data-product-id="${product.id}">${product.id} ↓</td>
                <td class="${productStatus === 'NOT COMPLETE' ? 'status-incomplete' : ''}">
                    ${productStatus}
                </td>
            `;

            // File details row
            const fileRow = document.createElement("tr");
            fileRow.classList.add("file-row");
            fileRow.style.display = "none";
            fileRow.innerHTML = `
                <td colspan="2">
                    <table border="1" width="100%">
                        <thead>
                            <tr>
                                <th>File Name</th>
                                <th>First Pass Status</th>
                                <th>Face Swap Status</th>
                                <th>Hand Fix Status</th>
                                <th>Upscale Status</th>
                            </tr>
                        </thead>
                        <tbody id="file-list-${product.id}">
                            ${createFileRows(product.images, product.id)}
                        </tbody>
                    </table>
                </td>
            `;

            tableBody.appendChild(productRow);
            tableBody.appendChild(fileRow);
        });

        // Add click handlers for expandable rows
        document.querySelectorAll(".expandable").forEach(item => {
            item.addEventListener("click", function () {
                const fileRow = this.parentNode.nextElementSibling;
                fileRow.style.display = fileRow.style.display === "none" ? "table-row" : "none";
            });
        });

    } catch (error) {
        console.error("Error loading products:", error);
    }
});