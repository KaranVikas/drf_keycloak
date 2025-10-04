import React, {useState} from 'react'
import {apiService} from '../services/apiService'
import type { RegisterFormData, RegisterFormProps } from '../services/apiService';

const RegisterForm: React.FC<RegisterFormProps> = ({ onSuccess, onCancel }) => {
  const [formData, setFormData ] = useState<RegisterFormData>({
    username: '',
    email: '',
    password: '',
    password_confirm: '',
    name: '',
  })

  const [errors, setErrors] = useState<Record<string, string[]>>({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const {name , value} = e.target
    setFormData(prev => ({...prev, [name]:value}));
    //   clear error when user starts typing
    if(errors[name]){
      setErrors(prev => ({...prev, [name]:[]}))
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setErrors({})

     try{
      await apiService.registerUser(formData);
      alert('Registration successful! you can now login');
      onSuccess?.()
     } catch (error: any){
      if(error.response?.data){
        setErrors(error.response.data);
      } else {
        setErrors({general: ['Registration  failed. Please try again.']})
      }
     } finally {
      setIsLoading(false);
     }
  };

  const renderFieldError = (fieldName: string) => {
    if(errors[fieldName]) {
      return(
          <div className="container-fluid d-flex jsutify-content-center align-items-center min-vh-100">
            <div className="col-md-6 col-lg-4">
              <div className="card shadow-lg">
                <div className="card-body p-4">
                  <h2 className="card-title text-center mb-4">Create Account</h2>

                  {errors.general && (
                      <div className="alert alert-danger" role="alert">
                        {errors.general.join(', ')}
                      </div>
                  )}

                  <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                      <label htmlFor="username" className="form-label">
                        Username <span className="text-danger">*</span>
                      </label>
                      <input
                        type="text"
                        id="username"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        className={`form-control ${errors.username ? 'is-invalid' : ''}`}
                        required
                        disabled={isLoading}
                      />
                      {renderFieldError('username')}
                    </div>
                    <div className="mb-3">
                      <label htmlFor="email" className="form-label">
                        Username <span className="text-danger">*</span>
                      </label>
                      <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        className={`form-control ${errors.email ? 'is-invalid' : ''}`}
                        required
                        disabled={isLoading}
                      />
                      {renderFieldError('email')}
                    </div>
                    <div className="mb-3">
                      <label htmlFor="name" className="form-label">
                        Username <span className="text-danger">*</span>
                      </label>
                      <input
                        type="text"
                        id="name"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        className={`form-control ${errors.name ? 'is-invalid' : ''}`}
                        required
                        disabled={isLoading}
                      />
                      {renderFieldError('name')}
                    </div>
                    <div className="mb-3">
                      <label htmlFor="password" className="form-label">
                        Username <span className="text-danger">*</span>
                      </label>
                      <input
                        type="password"
                        id="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        className={`form-control ${errors.password ? 'is-invalid' : ''}`}
                        required
                        disabled={isLoading}
                      />
                      {renderFieldError('password')}
                    </div>

                    <div className="d-grip gap-2">
                      <button
                        type="submit"
                        disabled={isLoading}
                        className={"btn btn-primary"}
                      >
                        {isLoading ? (
                            <>
                              <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true">
                                Creating Account...
                              </span>
                            </>
                        ) : (
                            'Create Account'
                        )}
                      </button>

                      {onCancel && (
                          <button
                            type="button"
                            onClick={onCancel}
                            disabled={isLoading}
                            className="btn btn-secondary"
                          >
                            Cancel
                          </button>
                      )}
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
      )
    }
  }
}

export default RegisterForm