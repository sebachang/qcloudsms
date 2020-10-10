const moment = require('moment')

export function getDateRange(days, format = 'YYYY-MM-DD') {
  let d = days
  let u = 'd'
  if (typeof (days) === 'string') {
    const arr = days.split(' ')
    if (arr.length === 2) {
      d = parseInt(arr[0])
      u = arr[1]
    }
  }
  const end = moment()
  const start = moment().subtract(d, u)
  if (format === undefined) {
    return [start, end]
  } else {
    return [start.format(format), end.format(format)]
  }
}
