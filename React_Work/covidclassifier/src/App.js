import {useState} from 'react';

function App() {
  const [file,setFile] = useState(null);
  const [res,setResponse] = useState(0);
  const handleFileChange = (event)=>{
    setFile(event.target.files[0]);
  }

  const handleUpload = async() => {
    if(!file) return;

    const data = new FormData();
    data.append('file',file);

    try{
      await fetch("http://localhost:5000/predict",{
        method: 'POST',
        body: data
      }).then(res=>{
        if(!res.ok){
          throw new Error("Network response not ok");
        }
        return res.json();
      }).then(data=>{
        setResponse(data.predictions[0][0]);
      })
      console.log(res)

    }
    catch(error){
      console.error("Error uploading file: ",error);
    }

  }

  return (
    <div className="App">
      {(res>0.5)?(
        <h1>Covid Negative</h1>
      ):(
        <h1>Covid Positive</h1>
      )}
      <input type="file" onChange={handleFileChange}/>
      <button onClick={handleUpload}>Upload</button>
      
    </div>
  );
}

export default App;
