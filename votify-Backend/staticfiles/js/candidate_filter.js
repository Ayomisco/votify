// js/candidate_filter.js

$(document).ready(function () {
    function fetchCandidates() {
        $('#loadingSpinner').show();  // Show spinner while loading
        var $jq = jQuery.noConflict();

        $.ajax({
            url: '/candidates/',
            data: {
                'election_type': $('#electionFilter').val()
            },
            success: function (data) {
                console.log(data);  // Log the response for debugging

                var candidateTable = $('#candidateTable tbody');
                candidateTable.empty();  // Clear the table before adding new rows

                if (data.candidates.length === 0) {
                    candidateTable.append('<tr><td colspan="5" class="text-center">No candidates available</td></tr>');
                } else {
                    $.each(data.candidates, function (index, candidate) {
                        var positionClass = '';
                        if (candidate.position === 'Winner') {
                            positionClass = 'winner';
                        } else if (candidate.position === 'Runner-up') {
                            positionClass = 'runner-up';
                        } else if (candidate.position === 'Second Runner-up') {
                            positionClass = 'second-runner-up';
                        } else if (candidate.position === 'No Votes Yet') {
                            positionClass = 'no-votes';  // Class for candidates with no votes
                        }
                        console.log(`Position Class: ${positionClass}`); // Add this line to debug
                        candidateTable.append(`
                            <tr class="">
                                <td>${index + 1}</td>
                                <td>${candidate.full_name}</td>
                                <td>${candidate.department}</td>
                                <td>${candidate.votes_count}</td>
                                <td><span class="btn ${positionClass} ">${candidate.position}</span></td>
                            </tr>
                        `);
                    });
                }

                $('#loadingSpinner').hide();  // Hide spinner after loading
            },
            error: function () {
                alert('Failed to fetch candidates.');
                $('#loadingSpinner').hide();  // Hide spinner on error
            }
        });
    }

    // Initial fetch
    fetchCandidates();

    // Fetch candidates based on election type filter
    $('#electionFilter').on('change', function () {
        fetchCandidates();
    });

    // Update vote counts asynchronously every 5 seconds
    setInterval(fetchCandidates, 5000);  // Poll every 5 seconds
});
