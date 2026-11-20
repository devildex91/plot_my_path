
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ActivityList from '../components/ActivityList.jsx';

const mockAttractions = [
  {
    id: 1,
    name: 'Eiffel Tower',
    entry_cost: 20,
    matches_preferences: true,
    image_url: '/images/eiffel-tower.jpg',
    description: 'Iconic landmark in Paris.',
  },
  {
    id: 2,
    name: 'Louvre Museum',
    entry_cost: 10,
    matches_preferences: false,
    image_url: '/images/louvre-museum.jpg',
    description: 'Famous art museum in Paris.',
  },
];

const mockActivities = [
  {
    id: 101,
    attraction_id: 1,
    start_time: '2026-11-19T09:00:00',
    end_time: '2026-11-19T10:00:00',
  },
  {
    id: 102,
    attraction_id: 2,
    start_time: '11:00:00',
    end_time: '12:00:00',
  },
];

describe('ActivityList', () => {
  it('displays the activities and their attraction names', () => {
    render(
      <ActivityList
        activities={mockActivities}
        attractions={mockAttractions}
        onRemove={vi.fn()}
        deletingActivityId={null}
        error={null}
      />
    );

    expect(screen.getByText('Eiffel Tower')).toBeInTheDocument();
    expect(screen.getByText('Louvre Museum')).toBeInTheDocument();
  });

  it('displays activity start and end times', () => {
    render(
      <ActivityList
        activities={mockActivities}
        attractions={mockAttractions}
        onRemove={vi.fn()}
        deletingActivityId={null}
        error={null}
      />
    );

    expect(screen.getByText(/09:00/)).toBeInTheDocument();
    expect(screen.getByText(/10:00/)).toBeInTheDocument();
    expect(screen.getByText(/11:00/)).toBeInTheDocument();
    expect(screen.getByText(/12:00/)).toBeInTheDocument();
  });

  it('displays the attraction entry costs', () => {
    render(
      <ActivityList
        activities={mockActivities}
        attractions={mockAttractions}
        onRemove={vi.fn()}
        deletingActivityId={null}
        error={null}
      />
    );

    expect(screen.getByText('£20pp')).toBeInTheDocument();
    expect(screen.getByText('£10pp')).toBeInTheDocument();
  });

  it('displays a preference match indicator when applicable', () => {
    render(
      <ActivityList
        activities={mockActivities}
        attractions={mockAttractions}
        onRemove={vi.fn()}
        deletingActivityId={null}
        error={null}
      />
    );

    expect(screen.getByText('Matches your interests')).toBeInTheDocument();
  });

  it('displays a fallback when an attraction cannot be found', () => {
    render(
      <ActivityList
        activities={[
          {
            ...mockActivities[0],
            attraction_id: 999,
          },
        ]}
        attractions={mockAttractions}
        onRemove={vi.fn()}
        deletingActivityId={null}
        error={null}
      />
    );

    expect(screen.getByText('Unknown attraction')).toBeInTheDocument();
  });

  it('calls onRemove with the activity ID when Remove is clicked', async () => {
    const user = userEvent.setup();
    const onRemove = vi.fn();

    render(
      <ActivityList
        activities={mockActivities}
        attractions={mockAttractions}
        onRemove={onRemove}
        deletingActivityId={null}
        error={null}
      />
    );

    const removeButtons = screen.getAllByRole('button', {
      name: 'Remove',
    });

    await user.click(removeButtons[0]);

    expect(onRemove).toHaveBeenCalledWith(101);
  });

  it('disables all Remove buttons while an activity is being deleted', () => {
    render(
      <ActivityList
        activities={mockActivities}
        attractions={mockAttractions}
        onRemove={vi.fn()}
        deletingActivityId={101}
        error={null}
      />
    );

    const buttons = screen.getAllByRole('button');

    expect(buttons).toHaveLength(2);
    buttons.forEach((button) => {
      expect(button).toBeDisabled();
    });

    expect(buttons[0]).toHaveClass('loading');
  });

  it('displays an error message when an error is provided', () => {
    render(
      <ActivityList
        activities={mockActivities}
        attractions={mockAttractions}
        onRemove={vi.fn()}
        deletingActivityId={null}
        error="Unable to remove activity."
      />
    );

    expect(screen.getByRole('alert')).toHaveTextContent(
      'Unable to remove activity.'
    );
  });

  it('displays an empty message when there are no activities', () => {
    render(
      <ActivityList
        activities={[]}
        attractions={mockAttractions}
        onRemove={vi.fn()}
        deletingActivityId={null}
        error={null}
      />
    );

    expect(
      screen.getByText('No activities planned for this day yet.')
    ).toBeInTheDocument();
  });
});
