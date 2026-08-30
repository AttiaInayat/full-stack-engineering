const Card = (props) => {
  return (
    <div className="card">
      <img src={props.img} alt="img" />
      <h2>
        {props.name}, {props.age}
      </h2>
      <p>
        Lorem ipsum dolor sit, amet consectetur adipisicing elit. Dolor, aperiam
        ad. Obcaecati, sint consectetur?
      </p>
      <button>View Profile</button>
    </div>
  );
};

export default Card;
