"use client";
import { useState, useEffect } from 'react';
import './style.css';

interface ErddapResponse {
  table: {
    columnNames: string[];
    rows: string[][]; // You can refine this type if you know the expected structure
  };
}

type ColumnRenderConfig = {
  label: string;
  className?: string;
  render?: (value: string) => React.ReactNode; 
}

export default function Home() {
  const [erddapResponse, setErddapResponse] = useState<ErddapResponse | null>(null);

  const url = "https://www.ncei.noaa.gov/erddap/griddap/index.json";
  const params = new URLSearchParams({
    page: '1',
    itemsPerPage: '50',
    "Dataset ID": "" // You can specify a dataset ID here if needed
  });

  function truncateString(str: string, maxLength: number=15): string {
    return str.length > maxLength
      ? str.slice(0, maxLength) + "..."
      : str;
  }
  
  function togglePopup(content: string = "") {
    const popup = document.getElementById("popup");
    const popupBody = document.getElementById("popup-body");
    if (popup && popupBody) {
      popup.classList.toggle("show");
      popupBody.innerHTML = content;
    }
  }
  
  const columnRenderMap: Record<string, ColumnRenderConfig> = {
    griddap: {
      label: "GRIDDAP DATA",
      className: "highlight-title",
      render: (value) => <a href={value} target="_blank" rel="noopener noreferrer">data</a>,
    },
    subset: {
      label: "Subset"
    },
    tabledap: {
      label: "Table DAP Data"
    },
    make_a_graph: {
      label: "Make A Graph",
      render: (value) => value
      ? <a href={value} target="_blank" rel="noopener noreferrer">graph</a>
      : ""
    },
    wms: {
      label: "WMS"
    },
    files: {
      label: "Source Data Files"
    },
    title: {
      label: "Title",
      render: (value) => <p className='content'>{value}</p>
    },
    summary: {
      label: "Summary",
      render: (value) => <button onClick={() => togglePopup(value)}>Summary</button>
    },
    info: {
      label: "Meta Data",
      render: (value) => <a href={value} target="_blank" rel="noopener noreferrer">M</a>,
    },
    background_info: {
      label: "Background Info",
      render: (value) => <a href={value} target="_blank" rel="noopener noreferrer">Background</a>,
    },
    rss: {
      label: "RSS",
      render: (value) => <a href={value} target="_blank" rel="noopener noreferrer"><img src="./rss.gif" alt="rss img" /></a>
    },
    institution: {
      label: "Institution",
      render: (value) => <p>{truncateString(value)}</p>
    },
    dataset_id: {
      label: "Dataset Id",
      render: (value) => <p className='content'>{value}</p>
    },
  }; 

  // Function to normalize column names
  function normalizeColumnName(name: string): string {
    return name
      .toLowerCase()
      .replace(/\s+/g, '_')     // Replace spaces with underscores
      .replace(/[^a-z0-9_]/g, ''); // Remove special characters if needed
  }

  // Function to fetch data from ERDDAP
  async function fetchErddapData(): Promise<void> {
    try {
      const response = await fetch(`${url}?${params.toString()}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data: ErddapResponse = await response.json();
      data.table.columnNames = data.table.columnNames.map(normalizeColumnName)
      setErddapResponse(data);

    } catch (error) {
      console.error("Error fetching ERDDAP data:", error);
    }
  }

  useEffect(() => {
    fetchErddapData();
  }, []);
  
  return (
    <div>
      <main>
        <div className='header'>
          <a href="https://www.noaa.gov/">
            <img className='header_image' src="./noaab.png" alt="noaab Logo" />
          </a>
          <div className='header_text'>
            <h1>ERDDAP</h1>
            <h2>Easier access to scientific data</h2>
          </div>
          <p>Brought to you by
            <a href='https://www.noaa.gov/' target="_blank" rel="noopener noreferrer">NOAA</a>  
            <a href='https://www.fisheries.noaa.gov/' target="_blank" rel="noopener noreferrer">NMFS</a>  
            <a href='https://www.fisheries.noaa.gov/about/southwest-fisheries-science-center' target="_blank" rel="noopener noreferrer">SWFSC</a>
            <a href='https://www.fisheries.noaa.gov/about/environmental-research-division-southwest-fisheries-science-center' target="_blank" rel="noopener noreferrer">ERD</a>
          </p>
        </div>
        <div className='body_text'>
          <h1>
          <a href='/errdap'>
            ERDDAP
          </a> / griddap</h1>
          <p>
            Griddap lets you use the OPeNDAP hyperslab protocol to request 
            data subsets, graphs, and maps from gridded datasets (for example, 
            satellite data and climate model data). For details, see:
          </p>
          <a href='https://www.ncei.noaa.gov/erddap/griddap/documentation.html' target="_blank" rel="noopener noreferrer">
            - ERDDAP's griddap Documentation.
          </a>
        </div>
        <div id='popup' className="popup">
          <div className="popup-content">
            <div className='popup-body'>
              <h1>Summary:</h1>
              <p id='popup-body'>Griddap lets you use the OPENDAP hyperslab protocol to request
            data subsets, graphs, and maps from gridded datasets (for example, 
            satellite data and climate model data). For details, see:</p>
            </div>
            <button className="popup-close" onClick={() => togglePopup("")}>close</button>
          </div>
        </div>
        <table>
          <thead>
            <tr>
              {erddapResponse?.table.columnNames.map((column, colIndex) => (
                <th key={colIndex}>
                  {columnRenderMap[column]?.label ?? column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {erddapResponse?.table.rows.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {row.map((value, colIndex) => {
                  const columnName = erddapResponse.table.columnNames[colIndex];
                  const config = columnRenderMap[columnName] || {};
                  return (
                    <td key={colIndex} className={config.className ?? ""}>
                      {config.render ? config.render(value) : value}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
        <div className='body_text'>
          <p>
            The information in the table above is also available in 
            other file formats (.csv, .htmlTable, .itx, .json, .jsonlCSV1, 
            .jsonlCSV, .jsonlKVP, .mat, .nc, .nccsv, .tsv, .xhtml)
            <a href='https://www.ncei.noaa.gov/erddap/rest.html' target="_blank" rel="noopener noreferrer">
              via a RESTful web service.
            </a>
          </p>
        </div>
          <footer>
            <p>ERDDAP, Version 2.23</p>
            <p>
              <a href='https://www.ncei.noaa.gov/erddap/legal.html' target="_blank" rel="noopener noreferrer">
                Disclaimers
              </a>
              | 
              <a href='https://www.ncei.noaa.gov/erddap/legal.html#privacyPolicy' target="_blank" rel="noopener noreferrer">
                Privacy Policy
              </a>
              | 
              <a href='https://www.ncei.noaa.gov/erddap/legal.html#contact' target="_blank" rel="noopener noreferrer">
                Contact
              </a>    
            </p>
          </footer>
      </main>
    </div>
  );
}
