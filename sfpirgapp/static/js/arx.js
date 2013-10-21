$(function() {
	function updateProjectButtons(selectedProjectIds) {
		$('a.arx-project-select').show();
		$('a.arx-project-deselect').hide();


		if (selectedProjectIds.length) {
			$('.category-tools').show();
			$('.selected-projects-count').html(selectedProjectIds.length);
		} else {
			$('.category-tools').hide();
		}

		$.each(selectedProjectIds, function(index, projId) {
			$('#arx-project-select-' + projId).hide();
			$('#arx-project-deselect-' + projId).show();
		});
	}


	function toggle(projId, value) {
		$.ajax({
			type: projId?'post':'get',
			dataType: 'json',
			url: '/arx/project/toggle-selection/' + projId + '/?random=' + Math.random(),
			data: {
				include: value
			}
		}).done(function(data) {
			updateProjectButtons(data.selected_projects);
		}).fail(function(error) {
			console.log('Failed. Error: ' + error);
		});
	}


	$('a.arx-project-select').click(function() {
		var projId = $(this).attr('id').substring('arx-project-select-'.length);
		toggle(projId, 'true');
		return false;
	});


	$('a.arx-project-deselect').click(function() {
		var projId = $(this).attr('id').substring('arx-project-deselect-'.length);
		toggle(projId, 'false');
		return false;
	});

	toggle(0, 'false');
});
