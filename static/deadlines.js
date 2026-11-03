// This runs once for every row in the table.
//   row          the table row (<tr>)
//   cell         the deadline cell (<td>)
//   opportunity  the row's data, including days_left from the server
//
// It adds an "Urgency" cell right after the deadline cell.
// The label only depends on days_left (team rule), not on the status.
function showDeadline(row, cell, opportunity) {
  const urgencyCell = document.createElement("td");
  cell.after(urgencyCell);

  const daysLeft = opportunity.days_left;
  let text = "";
  let colour = "";

  if (daysLeft < 0) {
    text = "Overdue";
    colour = "overdue";
  } else if (daysLeft === 0) {
    text = "Due today";
    colour = "today";
  } else if (daysLeft <= 7) {
    text = daysLeft === 1 ? "Due in 1 day" : "Due in " + daysLeft + " days";
    colour = "soon";
  }

  // Deadlines more than 7 days away get no label.
  if (text === "") {
    return;
  }

  const label = document.createElement("span");
  label.className = "deadline-label deadline-" + colour;
  label.textContent = text;
  urgencyCell.appendChild(label);
}

// Adds the "Urgency" column heading after the "Deadline" heading.
function addUrgencyHeading() {
  const headings = document.querySelectorAll("thead th");
  for (const heading of headings) {
    if (heading.textContent === "Deadline") {
      const urgencyHeading = document.createElement("th");
      urgencyHeading.textContent = "Urgency";
      heading.after(urgencyHeading);
    }
  }
}

addUrgencyHeading();
