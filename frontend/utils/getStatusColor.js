export default (status) => {
      if (status === 'CR') return 'blue'
      else if (status === 'WR') return 'orange'
      else if (status === 'PR') return 'green'
      else if (status === 'CL') return 'black'
      else return 'red'
}
