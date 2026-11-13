
    // script.js

    // Set data table pagination button count based on screen width
    if (window.innerWidth < 576) {
        $.fn.DataTable.ext.pager.numbers_length = 5; // Small screens
    } else if (window.innerWidth < 768) {
        $.fn.DataTable.ext.pager.numbers_length = 8; // Medium screens
    } else {
        $.fn.DataTable.ext.pager.numbers_length = 13; // Large screens
    }

    $(document).ready(function() {
        $('#content-table').DataTable({
            order: [], // Use existing order of the table
            pageLength: 25, // Show 25 rows per page
            lengthChange: true, // Allow user to change page length
            responsive: true, // Make table responsive
            autoWidth: false, // Prevent automatic column width
            language: {
                search: "Search records:",
                lengthMenu: "Show _MENU_ entries per page",
                info: "Showing _START_ to _END_ of _TOTAL_ entries"
            }
        });
    });

    $('.tdnn').click(function() {
        $("body").toggleClass('light');
        $(".moon").toggleClass('sun');
        $(".tdnn").toggleClass('day');
    });


    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".hoverable").forEach(function (el) {
            el.addEventListener("click", function (e) {
                // Close other tooltips
                document.querySelectorAll(".hoverable").forEach(function (other) {
                    if (other !== el) other.classList.remove("active");
                });

                // Toggle current tooltip
                el.classList.toggle("active");
            });
        });

        // Optional: Close tooltip when clicking outside
        document.addEventListener("click", function (e) {
            if (!e.target.closest(".hoverable")) {
                document.querySelectorAll(".hoverable").forEach(function (el) {
                    el.classList.remove("active");
                });
            }
        });
    });
    