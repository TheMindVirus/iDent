using UnityEngine;

public class Particle : MonoBehaviour
{
    public AudioSource audio_src = null;
    public Transform attract = null;
    public float speed = 0.01f;

    Vector3 diff;
    float radius = 0.0f;
    float thresh = 0.5f;

    void Start()
    {
        GameObject.DestroyImmediate(this.GetComponent<Collider>());
    }

    void Update()
    {
        if (attract != null)
        {
            diff = transform.position - attract.position;
            transform.position -= (diff * speed);
            radius = Vector3.Distance(transform.position, attract.position);
            if (radius < thresh)
            {
                if (audio_src != null)
                {
                    audio_src.Play();
                }
                Color chroma = this.GetComponent<Renderer>().material.GetVector("_Chroma");
                attract.gameObject.GetComponent<Renderer>().materials[1].SetVector("_Chroma", chroma);
                GameObject.DestroyImmediate(this.gameObject);
            }
        }
    }
}
