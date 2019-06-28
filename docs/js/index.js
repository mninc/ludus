$('.collapse').click(function() {
    let section = $('table').find(`tr[data-section='${this.dataset.toggles}']`);
    let link = $(this);
    if (section.css("display") === "none") {
        section.css("display", "table-row");
        link.text("Collapse");
    } else {
        section.css("display", "none");
        link.text("Expand");
    }
});
