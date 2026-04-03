// Function to parse a date string in the "year-month-day 12:00PM" format
export function parseDate(stringDate: string) {
    const [datePart, timePart] = stringDate.split(" ");
    const timeIn24HourFormat = convertTo24HourTime(timePart);
    const isoDateString = `${datePart}T${timeIn24HourFormat}`;
    return new Date(isoDateString);
}

function convertTo24HourTime(time: string) {
    const [timePart, meridian] = time.split(/(AM|PM)/i)
    let [hours, minutes] = timePart.split(":").map(Number)

    if (meridian.toUpperCase() === "PM" && hours != 12) {

        hours += 12; // Convert PM hours to 24-hour format
    }
    if (meridian.toUpperCase() === "AM" && hours === 12) {
        hours = 0; // Midnight case
    }

    return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}`;
}
