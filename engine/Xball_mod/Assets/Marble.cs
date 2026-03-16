using UnityEngine;

public class Marble : MonoBehaviour
{
    public float speed = 10.0f;

    Rigidbody body;
    Vector3 vector;

    void Start()
    {
        body = this.GetComponent<Rigidbody>();
    }

    void Update()
    {
        vector = Vector3.zero;
        vector.z += ((Input.GetAxis("Vertical")) * speed);
        vector.x += ((Input.GetAxis("Horizontal")) * speed);
        vector.z += ((Input.GetKey(KeyCode.W) ? 1.0f : 0.0f) * speed);
        vector.z -= ((Input.GetKey(KeyCode.S) ? 1.0f : 0.0f) * speed);
        vector.x -= ((Input.GetKey(KeyCode.A) ? 1.0f : 0.0f) * speed);
        vector.x += ((Input.GetKey(KeyCode.D) ? 1.0f : 0.0f) * speed);
        body.AddForce(vector);
    }
}
