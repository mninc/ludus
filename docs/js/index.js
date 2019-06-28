$('.collapse').click(function(){
    //let section = $(`#section-${this.dataset.section}`);
    let section = $('table').find(`tr[data-section='${this.dataset.toggles}']`);
    section.each(function(){console.log(this)});
    console.log(section);
    let link = $(this);
    if (section.css("display") === "none") {
        section.css("display", "table-row");
        link.text("Collapse");
    } else {
        section.css("display", "none");
        link.text("Expand");
    }
});
