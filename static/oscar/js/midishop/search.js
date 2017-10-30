'use strict';
$(document).ready(function(){
  function collapseSearchPanels() {
    if ($(window).width() < 768) {
      $('.search-panel-collapse').collapse('hide');
    } else {
      $('.search-panel-collapse').collapse('show');
    }
  }

  $(window).on('resize', function(){
    collapseSearchPanels();
  });
});
