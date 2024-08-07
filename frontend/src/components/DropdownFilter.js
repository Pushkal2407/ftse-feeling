//filter news stories according to criteria 

import React, { useState } from 'react';


const DropdownFilter = () => {
  const [filter, setFilter] = useState('');

  const handleChangeFilter = event => {
    setFilter(event.target.value); // Updating 'filter' state with the selected value from the dropdown
  }

  return (
    <div className='filter-button'>
      <label htmlFor="filter">Filter: </label>
      <select
        name="filter"
        value={filter}
        onChange={handleChangeFilter}
      >
        {/* default empty option for filtering, followed by 3 options for filtering by name, date and category */}
        <option value=""></option>
        <option value="name">Name</option>
        <option value="date">Date</option>
        <option value="category">Category</option>
      </select>
    </div>
  )
};

export default DropdownFilter;
