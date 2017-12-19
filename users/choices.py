USER_TYPES = (
        ( 0, 'participant'),
        ( 1, 'reviewer'),
        ( 2, 'admin'),
    )

REVIEW_STATUS = (
		(-1, 'submission_not_made'),
		(0, 'submission_in_review'),
		(1, 'submission_back_from_review'),
		(2, 'submission_approved')
	)

STATUS = (
		(0, 'submission_for_review'),
		(1, 'finished_review'),
		(2, 'submission_approved')
	)