import { Vue } from "vue"

export function confirmCallback(text, callback, rejectCallback = null) {
  if (confirm(text)) {
    callback()
  } else if (rejectCallback !== null) {
    rejectCallback()
  }
}

export function confirmPromise(text) {
  const promise = new Promise((resolve, reject) => {
    confirm(text) ? resolve() : reject()
  })

  return promise
}
